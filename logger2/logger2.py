import Cavity
from ule_status import get_ule_status

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import time

logger2_address = ""
collector_address = ""

cavities = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger2/inquiries")

def on_message(client, userdata, msg):

    statuses = {}
    
    for cavity in cavities:
        
        #make path some kind of function of cavity name
        path = ""

        try:
            status = get_ule_status(cavity, path)
            statuses[cavity.name] = status
        except:
            print("failed to obtain " + cavity.name + " status :(")

    #maintaining for testing
    
    #statuses = [True, True, True, False]
    
    #format the string; has to be a string, cannot be another variable (e.g. dictionary)
    #but we can make it emulate a dictionary by splitting key:value with colons and quadruplets with commas:
    #also for IFTTT purposes, we need to label each with a 'valuen' tag
    
    #so, the format for this is as follows: valuen:description:threshold:measured value
        
    #probably easiest to loop over statuses for this, but the valuen makes that a bit harder idk
    
    result_return = "value4:780 Master Status:1E-9:" + str(m_status) + ",value5:780 Cooling Status:0.4:" + str(c_status) + ",value6:780 Repump Status:1.2:" + str(r_status)
    
    #write to collector
    
    publish.single("logger2/results", result_return, hostname=collector_address)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger2_address, 1883, 60)

client.loop_forever()
