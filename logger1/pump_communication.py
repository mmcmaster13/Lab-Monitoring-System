import serial, time

from pump_communication_methods import request_spc_meas

import serial.tools.list_ports

import serial

def get_pressure():

    '''  c, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))'''

    ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 5)

    request = "~ 05 0B 00"

    ser.write(("%s\r" % request).encode())

    tt_return = ser.readline().decode()

    ser.close()

    if len(tt_return) > 0:
        
        components = tt_return.split(" ")
        pressure = float(components[3])
        unit = components[4]
        
        print("successful pump communication: " + tt_return)
        
    else:
        print("connection timed out, no return")
        
        pressure = 999.0
        
    return pressure

get_pressure()
