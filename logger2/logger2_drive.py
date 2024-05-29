import Cavity
from ule_status import get_ule_status

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import time

from spreadsheet_managing import write_locally, push_to_drive

logger2_address = ""
collector_address = ""

cavities = []

fields = ["Cavity1 Status","Cavity2 Status","Cavity3 Status","Cavity4 Status"]
source_path_stem = ""
header_flag = True

path = ""

destination_path_stem = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("logger2/inquiries")
    client.subscribe("publish_requests")

def on_message(client, userdata, msg):

    if msg.payload == "data please <3":

        statuses = {}
        
        for cavity in cavities:
            
            #make path some kind of function of cavity name
            image_path = ""

            try:
                status = get_ule_status(cavity, image_path)
                statuses[cavity.name] = status
            except:
                print("failed to obtain " + cavity.name + " status :(")

        #maintaining for testing
        
        #statuses = [True, True, True, False]
        
        #since we're not using IFTTT anymore, we can use a "pure" dictionary:
        result_return = {"Cavity1 Status": statuses[0], "Cavity2 Status": statuses[1], "Cavity3 Status": statuses[2],"Cavity4 Status": statuses[3]}

        #write to spreadsheet
        header_flag, path, now = write_locally(result_return, fields, source_path_stem, header_flag)
        
        #write to collector
        
        publish.single("logger2/results", result_return, hostname=collector_address)

    else:
        push_to_drive(path, now, destination_path_stem)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger2_address, 1883, 60)

client.loop_forever()
