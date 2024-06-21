# Harsh Choudhary, 2103117
import utils

class Receiver:

    def __init__(self,zn,n,k,X,systematic=False):
        self.n = n
        self.field = zn
        self.k = k
        self.d = n-k+1
        self.t = (self.d-1)//2          # max errors
        self.X = X
        self.systematic = systematic

    def decode(self,C_tilde):
        assert len(C_tilde)%self.n==0, 'block code so received codes should be of length mutliple of block length'

        M_decoded = []
        self.message = ""
        for i in range(0,len(C_tilde),self.n):
            m_decoded = utils.BerlekampWelchAlgorithm(C_tilde[i:i+self.n],self.X,self.field,self.t,self.k)

            if len(m_decoded)==1 and m_decoded[0]==-1:
                self.message += f'More than correctable no. of errors (max_error_correctability = {self.t}) occured in block {int(i/self.n)}. Request retransmission of block {int(i/self.n)} (0-indexed)!\n'
                m_decoded *= self.k
                M_decoded += m_decoded
            elif self.systematic:
                M_decoded += [self.field.id(sum([self.field.multiply(m_decoded[power],self.field.id(x**power)) for power in range(len(m_decoded))])) for x in self.X[0:self.k]]
            else:
                M_decoded += m_decoded          # that entire block put as -1 -1 ... -1

        if self.message == "":
            self.message = "Successfully Decoded!\n"

        return M_decoded

    def decode_block(self,c_tilde):
        m_decoded = utils.BerlekampWelchAlgorithm(c_tilde,self.X,self.field,self.t,self.k)
        if len(m_decoded)==1 and m_decoded[0]==-1:
            m_decoded *= self.k
            return m_decoded
        return m_decoded if not self.systematic else [utils.evaluate_polynomials(m_decoded,point,self.field) for point in self.X[:self.k]]

# from FiniteField import Zq
# receiver = Receiver(Zq(7),7,4,[i for i in range(7)],True)
# C_tilde = [1, 2, 2, 1, 0, 3, 6, 5, 2, 5, 1, 4, 3, 1]
# print("C_possible:",receiver.decode(C_tilde))