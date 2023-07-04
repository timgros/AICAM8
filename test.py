

import PositionKalman as Kal


measurements = [-61.,-63.,-58.,-59.,-61.]
motions = [0.7079,0.89,0.501187,0.5623,0.7079]

measurement_sig = 0.001;
motion_sig = 1.;
mu = 0.;
sig = 1000.

for n in range(len(measurements)):
    mu, sig = Kal.update(mu, sig, measurements[n], measurement_sig)
    print('Update: [{}, {}]'.format(mu, sig))
    mu, sig = Kal.predict(mu, sig, motions[n], motion_sig)
    print ('Predict: [{}, {}]'.format(mu, sig))
    
print ('\n')
print ('Final result: [{} {}]'.format(mu, sig))

