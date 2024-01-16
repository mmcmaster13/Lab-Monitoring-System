from hat_methods import get_potential_difference

import matplotlib.pyplot as plt
import numpy as np
import time

import statistics as stats

#goals: we want to write a loop that will collect the signal from the Toptica Monitor Output for the locked and unlocked states
#first, let's look at the unlocked state

#let's sample for three minutes.
#so, if time.sleep() is measuring every 0.1s, this will be 10 measurements per second
#so we need a total of 10*3*60 = 1800 points

var_voltages = np.zeros(1800)
s = np.arange(1800)

for i in range(1800):
    point = get_potential_difference()
    var_voltages[i] = point
    time.sleep(0.1)
    
print(var_voltages)

print("average:", np.mean(var_voltages))
print("standard deviation:", np.std(var_voltages))

plt.plot(s, var_voltages)
plt.title("Monitor Output Voltages in Varying States (differential)")
plt.xlabel("time (s)")
plt.ylabel("signal (V)")
plt.show()

running_avg = np.zeros(1791)
variances = np.zeros(1791)
s_avg = np.arange(9,1800)

for j in range(1791):
    
    avg = np.mean(var_voltages[j:j+10])
    var = stats.variance(var_voltages[j:j+10])
    
    running_avg[j] = avg
    variances[j] = var
    
plt.plot(s_avg, running_avg)
plt.title("Averaged Monitor Output Voltages in Varying States (differential)")
plt.xlabel("time (s)")
plt.ylabel("signal (V)")
plt.show()

plt.plot(s_avg, variances)
plt.title("Variance of Monitor Output Voltages in Varying States (differential)")
plt.xlabel("time (s)")
plt.ylabel("variance (V)")
plt.show()

