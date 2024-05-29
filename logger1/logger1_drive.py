import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import random

from thermocouple_comms import get_tc_reading
from pump_communication import get_pressure
from current_sensor import read_current

from spreadsheet_managing import write_locally, push_to_drive

#for our purposes, we'll call this Pi logger1, which will be in charge of
#rb oven current supply readings
#main chamber pressure readings
#yb oven temperature readings

status_count = [0,0,0]

collector_address = ""
logger1_address = ""

fields = ["Main Chamber Pressure", "Yb Oven Temperature", "Rb Supply Current"]
source_path_stem = ""
header_flag = True

path = ""

destination_path_stem = ""

#then, we need to subscribe it to something called "logger1/inquiries"
#so, this Pi will be listening for the master pi to request logger1 measurements

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger1/inquiries")
    client.subscribe("publish_requests")
    
def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    if msg.payload == "data please <3":
    
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
        
        #since we're not using IFTTT anymore, we can use a "pure" dictionary:
        result_return = {"Main Chamber Pressure": pressure, "Yb Oven Temperature": temperature, "Rb Supply Current": current}

        #write to spreadsheet
        header_flag, path, now = write_locally(result_return, fields, source_path_stem, header_flag)
        
        #write to collector
        publish.single("logger1/results", result_return, hostname=collector_address)

    else:
        push_to_drive(path, now, destination_path_stem)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger1_address, 1883, 60)

client.loop_forever()
