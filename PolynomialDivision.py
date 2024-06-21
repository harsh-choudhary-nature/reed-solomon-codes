# Harsh Choudhary, 2103117
from copy import deepcopy

class PolynomialDivisionOverFiniteField:
    
    def __init__(self,zn,Pl,Ps):
    
        self.field = zn
        # the coefficients are in these lists with increasing power of X order
        self.dividend = Pl
        self.divisor = Ps
        assert len(self.divisor)>0, "division with empty polynomial"
        assert self.divisor[len(self.divisor)-1]>0, "leading coeff of divisor can't be zero"

    def solve(self):
        dividend = deepcopy(self.dividend)              
        divisor = deepcopy(self.divisor)                        
        dividend_index = len(dividend)-1
        quotient = [0 for i in range(len(dividend)-len(divisor)+1)]       # atmost degree made, and again in increasing fashion only, and may have leading zeros
        remainder = [0 for i in range(len(divisor)-1)]
        highest_divisor_power = len(divisor)-1

        while dividend_index>=highest_divisor_power:
            if dividend[dividend_index]==0:
                dividend_index -= 1
                continue
            
            quotient_new = self.field.multiply(self.field.multiplyInverse(divisor[highest_divisor_power]),dividend[dividend_index])
            # print(dividend_index, dividend, divisor,quotient_new)
            quotient[dividend_index-highest_divisor_power] = quotient_new
            for i in range(len(divisor)):
                dividend[dividend_index-highest_divisor_power+i] = self.field.add(dividend[dividend_index-highest_divisor_power+i],-self.field.multiply(quotient_new,divisor[i]))
            
            # -1 done already in the if conditional at top

        # dividend_index is highest_divisor_power-1
        while dividend_index>=0:
            remainder[dividend_index] = dividend[dividend_index]
            dividend_index -= 1

        return quotient,remainder
            

# test
# from FiniteField import Zq
# zn = Zq(7)
# dividend = [5,4,3,6,0,1,0]                  # 5 + 4x + 3x2 + 6x3 + x5
# divisor = [0,3,0,6]                         # 3x + 6x3

# poly = PolynomialDivisionOverFiniteField(zn,dividend,divisor)
# # quotient: 5 + 6x2
# # remainder: 5 + 3x + 3x2
# print(poly.solve())