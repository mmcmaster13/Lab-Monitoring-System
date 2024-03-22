import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

from make_useful import make_useful
from peak_finding import get_derivatives, threshold_data, find_peaks, res_test

#check that the scope is connected and get its address

resources = visa.ResourceManager("@py")
print(resources.list_resources())

#do an *IDN? query to see if the scope will talk

rigol = resources.open_resource('USB0::6833::1160::DS1BC141100096::0::INSTR')

#this command obliterates the scope settings (makes time scale super small, turns on channel 2 when it wasn't already on, adds a huge DC offset?
#um that's because it's literally a reset
#rigol.write("*RST")
print(rigol.query("*IDN?"))

#let's try to get some waveforms out of this thing

#"Set the channel source of waveform reading"
rigol.write(":WAV:SOUR CHAN1")
#tells us which channel it's set to read waveforms from
print(rigol.query(":WAV:SOUR?"))

#demands new time scale
#rigol.write(":TIM:SCAL 0.00002")

#confirms time scale was set correctly
print(rigol.query(":TIM:SCAL?"))

#time.sleep(20)

#this limits the number of points WAVeform:POINts can return
#NORM is default but I'll include the call anyway for robustness
rigol.write(":WAV:MODE MAX")

rigol.write(":WAV:FORM ASC")

n_points = int(rigol.query(":WAV:POIN?"))

print("number of points taken: ", n_points)

#essentially you can use WAVeform:POINts if you want a specific number of points rather than "entire range"

data = rigol.query(":WAV:DATA?")

print(data)

x_origin = float(rigol.query(":WAV:XOR?"))
x_inc = float(rigol.query(":WAV:XINC?"))

print("X origin:", x_origin, "s")
print("X increments:", x_inc, "s")

#x = np.arange(1400)
x = np.arange(x_origin, x_origin + n_points * x_inc, x_inc)
    
#keeping both thresholded and raw data just in case
useful_data = make_useful(data, n_points)

data_th = threshold_data(useful_data, n_points)

rigol.close()

derivatives = get_derivatives(data_th, n_points)
x_d = np.arange(x_origin + 2*x_inc, x_origin + (n_points-3)*x_inc, x_inc)

print(len(derivatives))

#let's plot to see how this works hehehehehe

plt.plot(x, data_th)
plt.plot(x_d, derivatives)
#plt.legend(("thresholded lock signal data", "SG-filtered data"))
plt.xlabel("s")
plt.ylabel("lock signal, V")
plt.title("Raw Lock Signal Data and its Derivative (from SG Filtering)")
plt.show()

'''peak_locations = find_peaks(derivatives, n_points)

peak_with_te = res_test(500, 0.1)

print(peak_with_te)

average_loc = np.mean(peak_with_te)
std_loc = np.std(peak_with_te)

print("Average:", average_loc)
print("Standard Deviation:", std_loc)'''