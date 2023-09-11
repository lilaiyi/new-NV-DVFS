import numpy as np
def  score(x,y):
        result =  np.abs((y-x)/y)
        result = np.mean(result,axis=0)
        return result
