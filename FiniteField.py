# Harsh Choudhary, 2103117

class Zq:
    
    def __init__(self,q:int):
        self.q = q

    def id(self,a:int)->int:
        return a%self.q

    def add(self,a:int,b:int)->int:
        return (a+b)%self.q

    def addInverse(self,a:int)->int:
        return (-a)%self.q
    
    def sub(self,a:int,b:int)->int:
        return (a+self.addInverse(b))%self.q
    
    def multiply(self,a:int,b:int)->int:
        return (a*b)%self.q
    
    def multiplyInverse(self,a:int)->int:
        return pow(a%self.q, -1, self.q)       # calculates the multiplicative inverse of a mod q when power is -ve
    
    def divide(self,a:int,b:int)->int:
        return (a*self.multiplyInverse(b))%self.q
    
# test
    
# zn = Zq(5)
# print(zn.add(2,8))
# print(zn.sub(2,8))
# print(zn.multiply(2,8))
# print(zn.divide(2,8))
# print(zn.addInverse(2))
# print(zn.multiplyInverse(2))