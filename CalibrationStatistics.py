import numpy as np
from scipy import stats

def CalibrationStatistics(yh,gt,Bh,Bgt):
    '''
    Different statistics/metrics for benchmarking calibration performance:
    rmse: Root-Mean-Square-Error
    nrmse: Normalized RMSE
    corr: Pearson correlation between calibrated and groundtruth samples
    deltaB: Froebinus norm between underyling and calculated calibration matrix B

    Inputs:
    yh: calibrated measurements, size [n x m]
    gt: ground-truth measurement, size [n x m]
    Bh: estimated calibration matrix, size [n x n]
    Bgt: ground-truth calibration matrix, size [n x n]

    returns dict holding the 4 metrics as described above
    '''
    S = {
        'rmse': rms(yh-gt),
        'nrmse': rms(yh-gt)/rms(gt),
        'corr': mean_row_wise_corr(yh,gt),
        'deltaB': np.linalg.norm(Bh-Bgt,ord='fro')
    }  
    return S

def rms(a):
    return np.sqrt( np.mean( (a)**2) )

def mean_row_wise_corr(a,b):
    r = np.zeros((a.shape[0],1))
    for i in range(a.shape[0]):
        r[i] = stats.pearsonr(a[i,:],b[i,:])[0]
    return np.mean(r)