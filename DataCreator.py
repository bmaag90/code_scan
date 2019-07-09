import numpy as np

class DataCreator():
    '''
    DataCreator:

    Generates random data of multiple sensors that are in rendezvous (they meet in space and time) with each other.
    The sensor are aligned in a calibration path, which can be used to calibrate the sensors over multiple hops.
    '''
    def __init__(self, numSamples, numSensors, numHops, noiseLowerBound, noiseUpperBound, calparLowerBound, calparUpperBound, phenLowerBound, phenUpperBound, randomSeed):
        self.numSamples = numSamples # number of samples per rendezvous (i.e. the samples two sensors measure at the same time and location)
        self.numSensors = numSensors # number of sensor per array (e.g. a typical sensor array could consist of low-cost O3, NO2 and temperature sensors)
        self.numHops = numHops # number of hops in the calibration chain
        self.noiseLowerBound = noiseLowerBound # lower bound on the noise standard deviation (gaussian noise with mean 0)
        self.noiseUpperBound = noiseUpperBound # upper bound "
        self.calparLowerBound = calparLowerBound # lower bound on the calibration parameter matrix B (sampled from uniform distribution) 
        self.calparUpperBound = calparUpperBound # upper bound "
        self.phenLowerBound = phenLowerBound # lower bound on the phenomena (air pollution concentrations) standard deviation (log-normal distribution with mean 0)
        self.phenUpperBound = phenUpperBound # upper bound "
        self.random_seed = randomSeed # numpy random seed 

        np.random.seed(randomSeed)

    def create_calibration_points(self):
        self.X = [] # uncalibrated sensor values
        self.Y = [] # reference measurements for calibration, either from groundtruth or virtual ones from freshly calibrated sensors
        self.trueB = [] # true underlying calibration matrix B
        self.P = [] # physical phenomena
        self.Noise = [] # noise in the sensor signals
        for i in range(self.numHops+1):
            
            # sampling new underlying calibration parameters B
            self.trueB.append( self.calparLowerBound + (self.calparUpperBound-self.calparLowerBound)*np.random.rand(self.numSensors,self.numSensors) )
            # sampling new underlying physical phenomena (i.e. air pollution concentrations) with log-normal dist.
            sigma = self.phenLowerBound + (self.phenUpperBound-self.phenLowerBound)*np.random.rand(1)
            self.P.append( np.random.lognormal(0, sigma, (self.numSensors,self.numSamples)) )
            # sampling sensor noise with normal dist.
            self.Noise.append(self.noiseLowerBound + (self.noiseUpperBound-self.noiseLowerBound)*np.random.random(1))
            # uncalibrated sensor samples
            lh = self.trueB[i]
            rh = (self.Noise[i]*np.random.randn(self.numSensors,self.numSamples)) + self.P[i]                     
            self.X.append( np.linalg.solve(lh,rh) )    

            # reference data
            if i == 0:
                self.Y.append(self.P[i])            
            else: # we use the uncalibrated measurements as temporary references of sensor at hop i-1, these will be calibrated during the multihop calibration process
                lh = self.trueB[i-1] # use B from previous uncalibrated sensor (at hop i-1)
                rh = (self.Noise[i-1]*np.random.randn(self.numSensors,self.numSamples)) + self.P[i]
                self.Y.append( np.linalg.solve(lh,rh) )  
           
    def get_train_data(self,hop):
        return self.X[hop], self.Y[hop]

    def get_test_data(self,hop):
        return self.Y[hop+1],self.P[hop+1]
    
    def get_true_B(self,hop):
        return self.trueB[hop]