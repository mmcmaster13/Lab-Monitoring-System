import bme280
import smbus2

port = 1
address = 0x77
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def get_vals():
    bme280_data = bme280.sample(bus,address)
    
    temp = bme280_data.temperature
    hum = bme280_data.humidity
    
    return temp, hum