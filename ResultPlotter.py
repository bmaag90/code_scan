import matplotlib.pyplot as plt
import numpy as np

def ResultPlotter(Results,statsToPlot,calibrationMethods,numRuns,numHops):
    '''
    Plots of the results from the multi-hop calibration
    Errorplots of different metrics (Y-axis; specified in config.json: "statsToPlot": ["deltaB","rmse","corr","nrmse"]) over hop id (X-axis)

    Inputs:
    Results: See MultihopCalibration.py
    statsToPlot: List containing strings of the statistics/metrics which should be plotted (any of ["deltaB","rmse","corr","nrmse"])
    calibrationMethods: List containing strings of the calibration methods used (any of ["scan","mls])
    numRuns: see DataCreator.py
    numHops: see DataCreator.py
    '''
    numStats = len(statsToPlot)    

    fig, axs = plt.subplots(numStats)
    for m in calibrationMethods:
        for s in range(numStats):
            stat = statsToPlot[s]
            SummarizedResult = np.zeros((numRuns,numHops)) # results: runs x hops
            for run in range(numRuns):
                curR = [d[stat] for d in Results[m + '_run_'+str(run)] if stat in d]
                SummarizedResult[run,:] = curR

            meanSummarizedResult = np.mean(SummarizedResult,axis=0)
            stdSummarizedResult = np.std(SummarizedResult,axis=0)

            if numStats > 1:
                axs[s].errorbar(np.arange(numHops), meanSummarizedResult,yerr=stdSummarizedResult, label=m)
                axs[s].set(ylabel=stat)
            else:
                axs.errorbar(np.arange(numHops), meanSummarizedResult,yerr=stdSummarizedResult, label=m)
                axs.set(ylabel=stat)

    plt.legend()
    plt.xlabel('hop-number')
    plt.show()
        