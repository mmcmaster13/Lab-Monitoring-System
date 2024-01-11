#documentation for USB-2001-TC: https://files.digilent.com/manuals/UL-Linux/python/hwov.html#tc

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag)
import matplotlib.pyplot as plt
import numpy as np

def get_tc_reading():
    # Get a list of available DAQ devices
    devices = get_daq_device_inventory(InterfaceType.USB)

    # Create a DaqDevice Object and connect to the device
    daq_device = DaqDevice(devices[0])
    daq_device.connect()

    # Get AiDevice and AiInfo objects for the analog input subsystem
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()

    #create instance of analog input device config; required to change parameters
    config = ai_device.get_config()

    #set the thermocouple type to K
    config.set_chan_tc_type(0,2)

    #read the temperature in C
    temp = ai_device.t_in(0, 1)
    
    print("successful thermocouple reading: ", temp)

    return temp

    daq_device.disconnect()
    daq_device.release()

'''temps = np.zeros(20)

for i in range(20):
    
    if i == 10:
        print("halfway")
        
    temp = get_tc_reading()
    temps[i] = temp

plt.plot(temps)
plt.ylabel("Temperature (C)")
plt.xlabel("Measurement Number")

plt.show()'''
