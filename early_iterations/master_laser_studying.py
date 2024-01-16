#script used to set the threshold on the acceptable variance on the peak positions shown on the trace from the scanning FP cavity for the 780 master laser

import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

import statistics as stats

from make_scope_return_useful_again import make_useful
from peak_finding import get_derivatives, threshold_data, find_peaks

#configuring the scope

resources = visa.ResourceManager("@py")
print(resources.list_resources())

rigol = resources.open_resource('USB0::6833::1200::DS2D193902418::0::INSTR')

#testing that we can communicate as expected

#ask identity
print(rigol.query("*IDN?"))

#turn on channel 1
rigol.write(":WAV:SOUR CHAN1")

print(rigol.query(":WAV:SOUR?"))

#ask for time scale of trace
print(rigol.query(":TIM:SCAL?"))

#ask for maximum number of points sampled in trace
rigol.write(":WAV:MODE MAX")

rigol.write(":WAV:FORM ASC")

#ask for actual number of points in trace
n_points = int(rigol.query(":WAV:POIN?"))

#ask for where the origin is on the trace
x_origin = float(rigol.query(":WAV:XOR?"))

#ask for time difference between sampled points
x_inc = float(rigol.query(":WAV:XINC?"))

print("X origin:", x_origin, "s")
print("X increments:", x_inc, "s")

#to plot the behavior, let's take 600 points every 0.1s, locked, then unlocked, etc., etc. 3 different times

var_positions = np.zeros(3400)
s = np.arange(3400)

print("beginning collection")

'''for k in range(6):
    
    print("beginning to collect")

    for i in range(600):
        data = rigol.query(":WAV:DATA?")
        
        useful_data = make_useful(data, n_points)
        data_th = threshold_data(useful_data, n_points)

        derivatives = get_derivatives(data_th, n_points)

        peak_locations_i = find_peaks(derivatives, n_points)
        
        var_positions[i+600*k] = peak_locations_i[0]*x_inc + x_origin
    
    print("time to change the lock state")
    
    if k == 6:
        print("done collecting data")
    elif k % 2 == 0: #thus need to start locked for maximum relocking cushion
        time.sleep(30)
    else:
        time.sleep(90)'''

for i in range(3400):

    #ask for the trace data
    data = rigol.query(":WAV:DATA?")
    
    useful_data = make_useful(data, n_points)
    data_th = threshold_data(useful_data, n_points)

    derivatives = get_derivatives(data_th, n_points)

    peak_locations_i = find_peaks(derivatives, n_points)
    
    var_positions[i] = peak_locations_i[0]*x_inc + x_origin
    
print("done collecting")
    
print("average:", np.mean(var_positions))
print("standard deviation:", np.std(var_positions))
print("variance:", stats.variance(var_positions))

plt.plot(s, var_positions)
plt.title("Peak Positions in Varying Lock States")
plt.xlabel("time (s)")
plt.ylabel("position (s)")
plt.show()

running_avg = np.zeros(3391)
variances = np.zeros(3391)
stds = np.zeros(3391)
s_avg = np.arange(9,3400)

for j in range(3391):
    
    avg = np.mean(var_positions[j:j+10])
    var = stats.variance(var_positions[j:j+10])
    stds_j = np.std(var_positions[j:j+10])
    
    running_avg[j] = avg
    variances[j] = var
    stds[j] = stds_j
    
plt.plot(s_avg, running_avg)
plt.title("Averaged Peak Positions in Varying States")
plt.xlabel("time (s)")
plt.ylabel("peak position (s)")
plt.show()

'''

plt.plot(s_avg, variances)
plt.title("Variance of Peak Positions in Varying States")
plt.xlabel("time (s)")
plt.ylabel("variance (V)")
plt.ylim(0,0.0000002)
plt.show()

plt.plot(s_avg, stds)
plt.title("Standard Deviations of Peak Positions in Varying States")
plt.xlabel("time (s)")
plt.ylabel("standard deviation (V)")
plt.ylim(0,0.0000002)
plt.show()
'''






