from DataCreator import DataCreator
from SCAN import scan
from MLS import mls
from CalibrationStatistics import CalibrationStatistics
from ResultPlotter import ResultPlotter
import numpy as np
import argparse
import json

'''
Main script for running experiment!
Run "python MultihopCalibration.py --config_file=config.json"
'''


'''
Get the config (json) file, see "config.json" for default one
'''
parser = argparse.ArgumentParser(description='Parse location of config file (json).')
parser.add_argument('--config_file', type=str, default='config.json',
                    help='path to json config file, see config.json for default')

args = parser.parse_args()
with open(args.config_file) as json_data_file:
    config = json.load(json_data_file)

Results = {}

'''
Main loop
'''
for run in range(config['numRuns']):
    # we use the run number as random seed
    randomSeed = run
    # create new data
    myDataCreator = DataCreator(config['numSamples'],
        config['numSensors'], 
        config['numHops'],
        config['noiseLowerBound'],
        config['noiseUpperBound'],
        config['calparLowerBound'],
        config['calparUpperBound'],
        config['phenLowerBound'],
        config['phenUpperBound'],
        randomSeed)
    myDataCreator.create_calibration_points()
    # loop of different calibration methods
    for m in config['calibrationMethods']:
        calMethod = locals()[m]
        calB = []
        calTestData = []
        calStats = []
        # loop over the hops, i.e. perform calibration hop-by-hop
        for hop in range(config['numHops']):    
            # get the data for calibration
            X,Y = myDataCreator.get_train_data(hop)

            if hop == 0:
                # in the first hop we calibrate the sensor array to the true values   
                calB.append(calMethod(X,Y))
            else:
                # in the following hops (hop > 0) we calibrate the array to the previously calibrated one
                calB.append(calMethod(X,virtY))
            Xt,GT = myDataCreator.get_test_data(hop)

            virtY = calB[hop].dot(Xt)
            calTestData.append(virtY)
            trueB = myDataCreator.get_true_B(hop)

            calStats.append(CalibrationStatistics(virtY,GT,calB[hop],trueB))

        Results.update({ m + '_run_'+str(run): calStats})

# plot the results
if config['statsToPlot']:
    ResultPlotter(Results,config['statsToPlot'],config['calibrationMethods'],config['numRuns'],config['numHops'])