import numpy as np

def scan(X,Y):
    '''
    Calculates the solution for the constrained regression called SCAN
    given in the publication: Maag et al. "SCAN: Multi-Hop Calibration for Mobile Sensor Arrays".

    In particuluar it solves:    min_B trace( (Y-BX)(Y-BX)^T ) subject to BXX^TB^T = YY^T

    Inputs:
    X: size [n x m] (n: nUmber of sensors, m: nUmber of samples) 
    Y: size [n x m]

    returns B: [n x n]
    '''
    Ux,Dx,Vx = np.linalg.svd(X,full_matrices=False)
    Uy,Dy,Vy = np.linalg.svd(Y,full_matrices=False)
    Dx = np.diag(Dx)    
    Dy = np.diag(Dy)
    Vx = np.transpose(Vx)
    Vy = np.transpose(Vy) 

    M = np.matmul( np.transpose(Vx), np.matmul(Vy, np.matmul(Dy,np.transpose(Dy))))     

    Um,_,Vm = np.linalg.svd(M,full_matrices=False) 
    Vm = np.transpose(Vm)

    U = np.matmul(Vm,np.transpose(Um))
    L = np.matmul(Uy,Dy)  
    T = np.matmul(U,np.linalg.inv(Dx))

    return np.matmul(L,np.matmul(T,np.transpose(Ux)))
    