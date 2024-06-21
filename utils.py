# Harsh Choudhary, 2103117
from itertools import chain
from LinearSystem import LinearSystemOverFiniteField
from PolynomialDivision import PolynomialDivisionOverFiniteField

def is_unique(L:list):
    return len(L) == len(set(L))

def vander(X:list,k:int,zq):
    assert is_unique(X), 'List to vander contains duplicate entries'

    # in python, 0**0 is 1 so no extra handling
    matrix = []
    for power in range(0,k):
        matrix.append([])
        for x in X:
            matrix[len(matrix)-1].append(zq.id(x**power))
    return matrix
    
def matrix_multiply(A,B,zq):
    if len(A)==0 and len(B)==0:
        return list()

    assert len(A[0])==len(B), 'Dimensions of matrix in multiply is not compatible'

    C = []
    for i in range(len(A)):
        C.append([])
        for j in range(len(B[0])):
            C[i].append(0)
            for k in range(len(B)):
                C[i][j] += zq.id(A[i][k]*B[k][j])
            
            C[i][j] = zq.id(C[i][j])
    return C

def transpose(A):
    if len(A)==0:
        return []
    C = [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]
    return C

def vec_to_mat(A):
    assert len(A)==0 or isinstance(A[0],int), 'argument is not 1d array'
    return [A]

def mat_to_vec(A):
    return list(chain(*A))

def hamming_distance(v1,v2):
    assert len(v1)==len(v2), "distance between 2 vectors of only same length is defined"
    return sum([int(v1[i]-v2[i] != 0) for i in range(len(v1))])

def BerlekampWelchAlgorithm(c_tilde,X,zq,t,k):
    # t is the max no. of errors
    # print("c_tilde:",c_tilde)
    # print(f"t={t},k={k},X={X}")
    # set up the linear system
    A = transpose(vander(X,t+k,zq))
    # print("Partial A:\n",A)
    for i in range(len(c_tilde)):
        for power in range(t):
            A[i].append(zq.multiply(zq.id(-c_tilde[i]),zq.id(X[i]**power)))

    # print("A:\n",A)
    b = [zq.multiply(c_tilde[i],zq.id(X[i]**t)) for i in range(len(X))]
    # print("b=",b)
    solver = LinearSystemOverFiniteField(zq,A,b)
    solution = solver.solve()

    if 'no_solution' in solution:
        return [-1]
    
    # some solution exists
    if solution['infinite_solution']:
        # substitute any value for all the free variables, say 0
        for var_index in range(len(A[0])):
            if solution[var_index].is_free:
                solution[var_index].add_constant(0)
        
        # now compute values of all other variables in terms of substituted values of free variable
        for var_index in range(len(A[0])):
            new_constant = solution[var_index].ans['constant']
            # it may be the original free variable, in which case it's list will be empty for dependency on other variables
            for other_free_var_index in solution[var_index].ans:
                if other_free_var_index != 'constant':
                    new_constant += zq.multiply(solution[var_index].ans[other_free_var_index],solution[other_free_var_index].ans['constant'])
            solution[var_index].add_constant(new_constant)      # essentially no change as the free variables were set to 0 anyways
    
    # now whether unique_solution or infinite_solution, the 'constant' property of all var_index gives the  required coefficient terms

    # Qx_coeffs = [solution[var_index].ans['constant'] for var_index in range(t+k)]   # a0 a1 ... a(t+k-1)
    # Ex_coeffs = [solution[var_index].ans['constant'] for var_index in range(t+k,len(A[0]))]
    Qx_coeffs = []
    Ex_coeffs = []

    for var_index in range(len(A[0])):
        if 'constant' not in solution[var_index].ans:
            # print("not in")
            continue
        # print("in")
        if var_index>=t+k:
            Ex_coeffs.append(solution[var_index].ans['constant'])
        else:
            Qx_coeffs.append(solution[var_index].ans['constant'])
    Ex_coeffs.append(1)        # since the leading coeff is 1, e0 e1 ... e(t-1) 1
    # print("Qx_coeffs:",Qx_coeffs)
    # print("Ex_coeffs:",Ex_coeffs)
    poly_div = PolynomialDivisionOverFiniteField(zq,Qx_coeffs,Ex_coeffs)
    mx_coeffs,rx_coeffs = poly_div.solve()
    # print("mx_coeffs:",mx_coeffs)
    # print("rx_coeffs:",rx_coeffs)

    if all(item==0 for item in rx_coeffs):
        c_possible = [zq.id(sum([zq.multiply(mx_coeffs[power],zq.id(x**power)) for power in range(len(mx_coeffs))])) for x in X]
        if hamming_distance(c_possible,c_tilde)<=t:
            return mx_coeffs

    return [-1]

def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def to_list(text,ignore_set):
    lst = []
    i = 0
    while i<len(text):
        # print("i=",i)
        if text[i] in ignore_set:
            # print(text[i],"in ignore set")
            while i<len(text) and text[i] in ignore_set:
                # print("i=",i)
                i+=1
            if i<len(text):
                lst.append("")
        else:
            if len(lst)==0:
                lst.append("")
            lst[len(lst)-1] = lst[len(lst)-1] + text[i]
            i += 1        
    return lst

def evaluate_polynomials(px_coeffs,point,zq):
    # px_coeff in order of increasing degree
    ans = 0
    power = 0
    for px_coeff in px_coeffs:
        ans = zq.add(ans,zq.multiply(px_coeff,zq.id(point**power)))
        power += 1
    return ans

# test
# from FiniteField import Zq
# print(vander([0,1,2,3],5,Zq(5)))
# A = [[1,0,1]
#      ,[0,2,0]]

# B = [[3,4],
#      [4,5],
#      [1,6]]

# print(matrix_multiply(A,B,Zq(5)))
# print(transpose(vec_to_mat([1,2,3])))
# print(transpose(B))
# print(vec_to_mat([1,2,3]))

# List of lists
# list_of_lists = [[1, 2, 3]]

# Flatten the list
# flattened_list = mat_to_vec(list_of_lists)

# print(flattened_list)

# lst = to_list(", , , 55  55   , 2 \n0  ",set([","," ","\n","\t"]))
# print(lst)