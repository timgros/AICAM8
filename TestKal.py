
import kalman as kal
import numpy as np

Output = list()

def callKalman(kFilter, X):
    
    
    
    print ("Filtered Data:" , kFilter.filter(x))
    Output.append(kFilter.filter(x))
    
    


kFilter = kal.KalmanFilter(0.008, 0.1)

#testData = [66,64,63,63,63,66,65,67,58]
measurements = [-61.,-63.,-58.,-59.,-61.]

print ('Mean Input', np.mean(measurements))
print ('STDDEV Input', np.std(measurements))
print ('Max Input', max(measurements))
print ('Min Input', min(measurements))


#Output = list()

for x in measurements:
    print ("Data",x)
    callKalman(kFilter, x)
 #   print ("Filtered Data:" , kFilter.filter(x))
 #   Output.append(kFilter.filter(x))
    
    
print ('Mean Output', np.mean(Output))
print ('STDDEV Output', np.std(Output))    
print ('Max Output', max(Output))
print ('Min Output', min(Output))

