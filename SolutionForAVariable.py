# Harsh Choudhary, 2103117

class SolutionForAVariable:
    
    def __init__(self,variable_index,is_free=True):
        self.var = variable_index
        self.is_free = is_free
        self.ans = dict()

    def add_to_ans(self,variable_index,coeff):
        self.ans[variable_index] = coeff

    def add_constant(self,constant):
        self.ans["constant"] = constant
        self.is_free = False