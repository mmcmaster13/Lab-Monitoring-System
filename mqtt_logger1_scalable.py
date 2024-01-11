import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import random

from thermocouple_comms import get_tc_reading
from pump_communication import get_pressure
from current_sensor import read_current

#for our purposes, we'll call this Pi logger1, which will be in charge of
#rb oven current supply readings
#main chamber pressure readings
#yb oven temperature readings

status_count = [0,0,0]

#then, we need to subscribe it to something called "logger1/inquiries"
#so, this Pi will be listening for the master pi to request logger1 measurements

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger1/inquiries")
    
def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    #it's really just not worth waiting around for these to read
    #if it's going to get resolved on its own, it will be resolved on the next iteration
    #else it's not going to get resolved even if we wait here
    
    try:
        pressure = get_pressure()
            
    except:
        print("failed to read pressure :(")
        pressure = 9999
    
    try:
        temperature = get_tc_reading()
        
    except:
        print("failed to read temperature :(")
        temperature = 9999
        
    try:
        current = read_current()
        
    except:
        print("failed to read current :(")
        current = 9999
    
    #maintaining for testing
    
    '''pressure = 1e-11
    temperature = random.randrange(21)
    current = 10'''
    
    #format the string; has to be a string, cannot be another variable (e.g. dictionary)
    #but we can make it emulate a dictionary by splitting key:value with colons and pairs with commas:
    #also for IFTTT purposes, we need to label each with a 'valuen' tag
    
    #so, the format for this is as follows: valuen:description:threshold:measured value
    
    result_return = "value1:Main Chamber Pressure:1E-9:" + str(pressure) + ",value2:Yb Oven Temperature:400:" + str(temperature) + ",value3:Rb Supply Current:8:" + str(current)
    
    #write to master; might want to change the name of the Pi from "logger1" to something more illustrative
    
    publish.single("logger1/results", result_return, hostname="192.168.0.184")
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.185", 1883, 60)

client.loop_forever()