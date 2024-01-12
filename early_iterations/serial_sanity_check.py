import serial

ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 5)

request = "*IDN?"

ser.write(("%s\r" % request).encode())
    
tt_return = ser.readline()

ser.close()

if len(tt_return) > 0:
    print("Success! " + tt_return.decode())
else:
    print("connection timed out, no return")