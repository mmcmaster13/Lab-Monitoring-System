#code that will be responsible for handling networking on the logger3 side of things

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import pyvisa as visa
from peak_counting import count_peaks

#for our purposes, we'll call this Pi logger4, which will be in charge of all the 780 lasers' lock statuses

resources = visa.ResourceManager("@py")
print(resources.list_resources())

collector_address = ""
logger4_address = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger4/inquiries")
    
def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    #it's really just not worth waiting around for these to read
    #if it's going to get resolved on its own, it will be resolved on the next iteration
    #else it's not going to get resolved even if we wait here

    rigol = resources.open_resource('USB0::6833::1160::DS1BC141100096::0::INSTR')
    
    try:
        p_count = count_peaks(rigol)
            
    except:
        print("failed to get status from Fabry-Perot setup :(")
        p_count = 9999
        
    rigol.close()
        
    #so, the format for this is as follows: valuen:description:threshold:measured value
    
    result_return = "value7:Number of Peaks on FP:" + str(p_count)
    
    #write to collector
    
    publish.single("logger4/results", result_return, hostname=collector_address)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger4_address, 1883, 60)

client.loop_forever()