from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
#from Phidget22.EnumerationType import *

import time

import numpy as np

def onSensorChange(self, sensorValue, sensorUnit):
    
    #if 0.1, then 0
    
    adjusted_value = np.round((sensorValue+0.607),1)
    
    print("SensorValue: " + str(adjusted_value))
    print("SensorUnit: " + str(sensorUnit.symbol))
    
    current = sensorValue
    
    #write current
    
    print("----------")
    
    return current

'''def main():
    voltageInput0 = VoltageInput()

    voltageInput0.setIsHubPortDevice(True)
    voltageInput0.setHubPort(0)

    voltageInput0.setOnSensorChangeHandler(onSensorChange)

    voltageInput0.openWaitForAttachment(5000)

    voltageInput0.setSensorType(VoltageSensorType.SENSOR_TYPE_3589)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    voltageInput0.close()'''
	
def read_current():
    
    #set up channel
    voltageInput0 = VoltageInput()

    voltageInput0.setIsHubPortDevice(True)
    voltageInput0.setHubPort(0)
    voltageInput0.openWaitForAttachment(5000)
    voltageInput0.setSensorType(VoltageSensorType.SENSOR_TYPE_3588)
    
    #get voltage
    voltage = voltageInput0.getVoltage()
    print(voltage)

    voltageInput0.close()
    
    #applying the voltage-to-current conversion
    current = (voltage*40)-100
    adj_current = np.round((current+0.607),1)
    
    print(adj_current)
    
    #voltageInput0.setOnSensorChangeHandler(onSensorChange)
    
    return adj_current