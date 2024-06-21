# Harsh Choudhary, 2103117
import numpy as np
from FiniteField import Zq

class Environment:
    def __init__(self,n,k,zq,X):
        self.n = n
        self.k = k
        self.d = self.n-k+1
        self.max_errors = 0
        self.field = zq
        self.X = X
        self.randomise = False

    def err(self,C):
        C_tilde = np.array([]).astype('int')
        for i in range(0,len(C),self.n):
            if self.randomise:
                v0 = np.random.randint(0,self.n+1)
            else:
                v0 = self.max_errors      # true no. of bit errors
            # print(v0)
            if v0==self.n:
                i0 = np.random.shuffle(np.array([i for i in range(self.n)]))
            else:
                i0 = np.random.choice(np.arange(0, self.n-1), size=v0, replace=False)
            # print(i0)
            et = np.random.choice(np.arange(1,self.field.q-1),size=v0)       # error introduced so can't be zero
            # print(et)
            e0 = np.zeros((self.n,)).astype(int)
            # print(e0.shape)
            # print(e0)
            e0[i0] = et
            # print(e0)
            c_tilde = ((C[i:i+self.n] + e0)%self.field.q)
            C_tilde = np.concatenate((C_tilde,c_tilde))
            # print(C_tilde)
    
        return C_tilde.tolist()
    
# C = [1, 2, 2, 1, 6, 3, 6, 5, 2, 5, 6, 4, 5, 1]
# environment = Environment(7,4,Zq(7),[i for i in range(7)])
# print(environment.err(C))