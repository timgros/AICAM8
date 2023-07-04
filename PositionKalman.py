
from math import *
import matplotlib.pyplot as plt
import numpy as np

def f(mu, sigma2, x):
    coefficient = 1.0 / sqrt(2.0 * pi * sigma2)
    exponential = exp(-0.5 * (x-mu)**2/sigma2)
    return coefficient * exponential

def update (mean1, var1, mean2, var2):
    new_mean = (var2*mean1 + var1 * mean2)/(var2 + var1)
    new_var = 1/ (1/var2 + 1/var1)
    
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    
    return [new_mean, new_var]

def kfilter(z, u=0):
    
    return 0
    
    
    

#measurements = [5.,6.,7.,9.,10.]
#motions = [1.,1.,2.,1.,1.]

#measurement_sig = 4.;
#motion_sig = 2.;
#mu = 0.;
#sig = 1000.

#for n in range(len(measurements)):
#    mu, sig = update(mu, sig, measurements[n], measurement_sig)
#    print('Update: [{}, {}]'.format(mu, sig))
#    mu, sig = predict(mu, sig, motions[n], motion_sig)
#    print ('Predict: [{}, {}]'.format(mu, sig))
    
#print ('\n')
#print ('Final result: [{} {}]'.format(mu, sig))


    



