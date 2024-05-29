#code that will be responsible for handling networking on the logger3 side of things

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import pyvisa as visa
from peak_counting import count_peaks

from spreadsheet_managing import write_locally, push_to_drive

#for our purposes, we'll call this Pi logger4, which will be in charge of all the 780 lasers' lock statuses

resources = visa.ResourceManager("@py")
print(resources.list_resources())

collector_address = ""
logger4_address = ""

fields = ["FP Peak Count"]
source_path_stem = ""
header_flag = True

path = ""

destination_path_stem = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger4/inquiries")
    client.subscribe("publish_requests")
    
def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    if msg.payload == "data please <3":

        rigol = resources.open_resource("")
        
        try:
            p_count = count_peaks(rigol)
                
        except:
            print("failed to get status from Fabry-Perot setup :(")
            p_count = 9999
            
        rigol.close()
            
        #so, the format for this is as follows: valuen:description:threshold:measured value
        
        result_return = {"Number of Peaks on FP":p_count}

        #write to spreadsheet
        header_flag, path, now = write_locally(result_return, fields, source_path_stem, header_flag)
        
        #write to collector
        publish.single("logger4/results", result_return, hostname=collector_address)

    else:
        push_to_drive(path, now, destination_path_stem)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger4_address, 1883, 60)

client.loop_forever()