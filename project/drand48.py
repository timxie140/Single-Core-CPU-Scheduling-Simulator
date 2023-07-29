import math

class Rand48(object):
    def __init__(self, seed, Lambda, upperLimit):
        self.seed = seed
        self.Labmda = Lambda
        self.upperLimit = upperLimit
        self.srand()
    
    #Srand to set the seed for the random number generator
    def srand(self):
        self.n = (self.seed << 16) + 0x330e
    
    #Next operation for the random number generator
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    
    #Combined with next() to generate a random number
    def drand(self):
        return self.next() / 2**48
    
    #Floor operation for the random number generator
    def floor(self):
        tmp_num = math.floor(-math.log(self.drand())/self.Labmda)
        while tmp_num > self.upperLimit:
            tmp_num = math.floor(-math.log(self.drand())/self.Labmda)
        return tmp_num
    
    #Ceil operation for the random number generator
    def ceil(self):
        tmp_num = math.ceil(-math.log(self.drand())/self.Labmda)
        while tmp_num > self.upperLimit:
            tmp_num = math.ceil(-math.log(self.drand())/self.Labmda)
        return tmp_num
