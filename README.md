# Code for "SCAN: Multi-Hop Calibration for Mobile Sensor Arrays"

This repository provides a simple framework to highlight the benefits of SCAN (see paper) over Multiple Least-Squares (MLS) when applied to multi-hop calibration.
In particular, it shows that SCAN minimizes error accumulation over multiple hops in constrast to MLS that suffers from the bias-towards-zero (also known as [regression dilution (wiki link)](https://en.wikipedia.org/wiki/Regression_dilution) problem and, thus, also error accumulation.

## Code Structure

Following files are provided:
* `MultihopCalibration.py`: Main experiment loop. Run `python MultihopCalibration.py --config_file=config.json` to start a new experiment
* `DataCeator.py`: Generates artificial data used to test the calibration methods. The data resembles measurements from cross-sensitive and noisy low-cost sensor-arrays that measure typical air pollution concentrations.
* `CalibrationStatistics.py`: Calculates different statistics/metrics to benchmark the performance of the calibration
* `ResultPlotter.py`: Plots the results of the calibration, in particular shows an errorbar plot of different metrics over the different hops within the calibration path.
* `MLS.py`: Calculates calibration parameters according to Multiple Least-Squares
* `SCAN.py`: Calculates calibration parameters according to SCAN
* `config.json`: Different configuration parameters used to perform the experiment

