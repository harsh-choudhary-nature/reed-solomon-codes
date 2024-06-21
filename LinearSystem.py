# Harsh Choudhary, 2103117
from copy import deepcopy
from FiniteField import Zq
from SolutionForAVariable import SolutionForAVariable

class LinearSystemOverFiniteField:
    def __init__(self,zn,A,b):

        assert len(A)==len(b)

        self.field = zn
        self.A = A          # (m,n), meaning m equations and n variables
        for i in range(len(A)):
            for j in range(len(A[i])):
                self.A[i][j] = self.field.id(A[i][j])

        self.b = b          # (m,1)
        for i in range(len(b)):
            self.b[i] = self.field.id(b[i])

    def augment(self):
        aug = deepcopy(self.A)
        for i in range(len(self.b)):
            aug[i].append(self.b[i])
        return aug

    def get_leftmost_topmost_non_zero_indices(self,mat,row_index_st):
        for col_index in range(0,len(mat[row_index_st])):
            for row_index in range(row_index_st,len(mat)):
                if mat[row_index][col_index]!=0:
                    return col_index,row_index
        return -1,-1
    
    def get_leading_one_col_index(self,mat,row_index):
        for col_index in range(0,len(mat[row_index])):
            if mat[row_index][col_index]!=0:
                return col_index
        return -1
    
    def interchange(self,mat,row_index1,row_index2):
        # inplace
        mat[row_index1], mat[row_index2] = mat[row_index2], mat[row_index1]

    def scalar_multiply(self,mat,row_index,constant):
        # inplace
        for col_index in range(len(mat[row_index])):
            mat[row_index][col_index] = self.field.divide(mat[row_index][col_index],constant)

    def add_multiple_of_other_row(self,mat,row_index,other_row_index,constant):
        # inplace
        for col_index in range(len(mat[row_index])):
            mat[row_index][col_index] = self.field.add(mat[row_index][col_index],self.field.multiply(mat[other_row_index][col_index],constant))

    def convert_to_ref(self,mat):
        for cur_row_index in range(0,len(mat)):
            # print("cur_row_index:",cur_row_index)
            pivot_col_index,top_most_row_index = self.get_leftmost_topmost_non_zero_indices(mat,cur_row_index)
            # print("pivot_col_index, topmost_row_index",pivot_col_index, top_most_row_index)
            if pivot_col_index==-1:
                break

            self.interchange(mat,cur_row_index,top_most_row_index)
            # print("After interchange\n",mat)
            pivot_element = mat[cur_row_index][pivot_col_index]
            self.scalar_multiply(mat,cur_row_index,pivot_element)
            # print("After scalar multiply\n",mat)
            for further_row_index in range(cur_row_index+1,len(mat)):
                self.add_multiple_of_other_row(mat,further_row_index,cur_row_index,-mat[further_row_index][pivot_col_index])
            # print("After add multiple of other row\n",mat)

        return mat
    
    def convert_to_rref(self,mat):
        mat = self.convert_to_ref(mat)
        # print("REF:_\n",mat)
        for cur_row_index in range(len(mat)-1,-1,-1):
            pivot_col_index = self.get_leading_one_col_index(mat,cur_row_index)
            for further_row_index in range(cur_row_index-1,-1,-1):
                self.add_multiple_of_other_row(mat,further_row_index,cur_row_index,-mat[further_row_index][pivot_col_index])
        return mat

    def solve(self):
        
        aug = self.augment()
        # print("Augmented Matrix\n",aug)
        rref_aug = self.convert_to_rref(aug)
        # print("RREF\n",rref_aug)
        # exit(0)

        soln = dict()
        if len(self.A)==0:
            return soln
        
        for var in range(0,len(self.A[0])):
            soln[var] = SolutionForAVariable(var)       # all variable are free by default
        
        soln["infinite_solution"] = False
        for cur_row_index in range(len(rref_aug)-1,-1,-1):
            pivot_col_index = self.get_leading_one_col_index(rref_aug,cur_row_index)
            if pivot_col_index==len(rref_aug[cur_row_index])-1:
                soln["no_solution"] = True
                return soln
            elif pivot_col_index==-1:
                continue
            
            # print("pivot_col_index:",pivot_col_index)
            soln[pivot_col_index].add_constant(rref_aug[cur_row_index][len(rref_aug[cur_row_index])-1])
            # print("soln[pivot_col_index].ans['constant']:",soln[pivot_col_index].ans["constant"])
            for free_var_index in range(pivot_col_index+1,len(self.A[cur_row_index])):
                # claim: Never can a dependent variable satisfy the if condition due to rref form 
                if rref_aug[cur_row_index][free_var_index]!=0:
                    
                    assert soln[free_var_index].is_free

                    soln[pivot_col_index].add_to_ans(free_var_index,rref_aug[cur_row_index][free_var_index])
                    # print("soln[pivot_col_index].ans[free_var_index]:",soln[pivot_col_index].ans[free_var_index])
                    soln["infinite_solution"] = True
        
        soln["unique_solution"] = not soln["infinite_solution"]
        self.soln = soln
        return soln
                        

# # test
# A = [[1,0,0],
#     [0,0,1],
#     [0,1,0]]
# b = [1,2,3]
# solver = LinearSystemOverFiniteField(Zq(5),A,b)
# solution = solver.solve()

# if "no_solution" in solution:
#     print("Inconsistent system of equations")
# elif solution["infinite_solution"]:
#     for variable_index in range(0,len(A[0])):
#         if not solution[variable_index].is_free:
#             ans = "X"+str(variable_index) + ' = '
#             for other_variable_index in solution[variable_index].ans:
#                 if other_variable_index=="constant":
#                     continue

#                 ans += f"({solution[variable_index].ans[other_variable_index]})X{other_variable_index} + "
#             ans += str(solution[variable_index].ans["constant"])
#             print(ans)
#         else:
#             print(f'X{variable_index} is free')
# else:
#     for variable_index in range(0,len(A[0])):
#         ans = f"X{variable_index} = {solution[variable_index].ans['constant']}"
#         print(ans)



# debugging app.py
# A = [[1,0,0],
#     [1,1,0],
#     [1,2,0]]
# b = [0,0,0]
# solver = LinearSystemOverFiniteField(Zq(7),A,b)
# solution = solver.solve()

# if "no_solution" in solution:
#     print("Inconsistent system of equations")
# elif solution["infinite_solution"]:
#     print("Infinite Solution")
#     for variable_index in range(0,len(A[0])):
#         if not solution[variable_index].is_free:
#             ans = "X"+str(variable_index) + ' = '
#             for other_variable_index in solution[variable_index].ans:
#                 if other_variable_index=="constant":
#                     continue

#                 ans += f"({solution[variable_index].ans[other_variable_index]})X{other_variable_index} + "
#             ans += str(solution[variable_index].ans["constant"])
#             print(ans)
#         else:
#             print(f'X{variable_index} is free')
# else:
#     print("Unique solution")
#     for variable_index in range(0,len(A[0])):
#         if 'constant' in solution[variable_index].ans:
#             ans = f"X{variable_index} = {solution[variable_index].ans['constant']}"
#             print(ans)
#         else:
#             break
