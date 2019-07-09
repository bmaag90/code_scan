import numpy as np

def mls(X,Y):
    '''
    Performs multiple least squares on raw sensor samples X and reference samples Y

    Inputs:
    X: size [n x m] (n: number of sensors, m: number of samples) 
    Y: size [n x m]

    returns B: [n x n]
    '''
    B,_,_,_ = np.linalg.lstsq(X.T,Y.T,rcond=None)
    return B.T