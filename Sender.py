# Harsh Choudhary, 2103117
import utils
from LinearSystem import LinearSystemOverFiniteField

class Sender:
    def __init__(self,zq,k,systematic:bool = False):
        self.field = zq
        self.k = k

        # default
        self.n = zq.q
        self.d = self.n-self.k+1    # MDS
        self.systematic = systematic

    def change_distance(self,d_new):
        n_new = d_new + self.k - 1
        if n_new>self.field.q:
            print(f'A distance of {d_new} is not achievable on field of size {self.field.q}')
            raise ValueError('d_new out of range')

        self.d = d_new
        self.n = self.k + self.d - 1
        
    def change_block_length(self,n_new):
        if n_new>self.field.q:
            print(f'Block Length {n_new} is not achievable on field of size {self.field.q}')
            raise ValueError('n_new out of range')

        self.n = n_new
        self.d = self.n - self.k + 1

    def get_evaluation_points(self):
        return [i for i in range(self.n)]
    
    def get_generator_matrix(self):
        X = [i for i in range(self.n)]
        return utils.vander(X,self.k,self.field)

    def encode(self,M:list)->list:
        # len(M) must be a multiple of k
        assert len(M)%self.k==0, 'Block codes need message length to be a multiple of k'
        
        if not all(item < self.field.q for item in M):
            raise ValueError('Message contains symbols outside the field, other than [{0},{field.q}-1]')
        
        X = [i for i in range(self.n)]
        G = utils.vander(X,self.k,self.field)           # can do like this as our sender will be able to send message only once

        C = []
        for i in range(0,len(M),self.k):
            if self.systematic:
                # need to get polynomial coefficients for p(x) by using p(Xi) = mi for i in [1,..,k]
                A = utils.transpose([G[i][:self.k] for i in range(len(G))])
                # print(A)
                # print(G)
                b = M[i:i+self.k]
                # print(b)
                lin_solver = LinearSystemOverFiniteField(self.field,A,b)
                solution = lin_solver.solve()
                # since square vandermonde matrix, so invertible, hence always a unique solution
                assert 'no_solution' not in solution and not solution['infinite_solution'], 'Invertible Vandermonde matrix always yields unique solution'
                poly_coeffs = [solution[variable_index].ans['constant'] for variable_index in range(0,self.k)]
                # print(poly_coeffs)
                c = utils.mat_to_vec(utils.matrix_multiply(utils.vec_to_mat(poly_coeffs),G,self.field))
                C += c
                # exit(0)
            else:
                # print(utils.vec_to_mat(M[i:i+self.k]))
                # print(G)
                c = utils.mat_to_vec(utils.matrix_multiply(utils.vec_to_mat(M[i:i+self.k]),G,self.field))
                C += c

        return C

# test
# from FiniteField import Zq
# sender = Sender(Zq(7),4,True)

# try:
#     print(sender.encode([1,2,2,1,5,2,5,6]))
# except ValueError:
#     print("Invalid")