import Cavity
from ule_status import get_ule_status
from bme280_interfacing import get_vals

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import datetime
import time

from spreadsheet_managing import write_locally, push_to_drive

logger2_address = "192.168.0.197"
collector_address = "192.168.0.194"

cavities = []

#fields = ["Cavity1 Status","Cavity2 Status","Cavity3 Status","Cavity4 Status"]
fields = ['Time','ULE Table Temperature', 'ULE Table Humidity']

header_flag = True
path = ""

source_path_stem = r'/media/rbyb/EA30-895D/'
destination_path_stem = r'/home/rbyb/mnt/gdrive/Lab Monitoring System/ULE Cavity Table Pi/'

now = datetime.date.today()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("logger2/inquiries")
    client.subscribe("publish_requests")

def on_message(client, userdata, msg):
    
    global header_flag
    global now
    
    payload = msg.payload.decode("utf-8")
    print(msg.topic+" "+ payload)

    '''if msg.payload == "data please <3":

        statuses = {}
        
        for cavity in cavities:
            
            #make path some kind of function of cavity name
            image_path = ""

            try:
                status = get_ule_status(cavity, image_path)
                statuses[cavity.name] = status
            except:
                print("failed to obtain " + cavity.name + " status :(")'''
    
    if payload == "data please <3":
        
        try:
            temp, hum = get_vals()
            
        except:
            
            "failed to communicate with BME280 :("
            temp = 9999
            hum = 9999

        now = datetime.date.today()
        time = datetime.datetime.now()
        stime = time.strftime("%c")
        
        result_return = [{'Time':stime,'ULE Table Temperature':temp,'ULE Table Humidity':hum}]
        result_publish = 'ULE Table Temperature, ULE Table,'+str(temp) + ";ULE Table Humidity, ULE Table," + str(hum)
        
        try:
        
            write_locally(result_return, fields,source_path_stem,header_flag)
            print("written locally!")
            
        except:
            
            print("failed to write locally. check destination path.")
        
        header_flag = False
        
        publish.single("logger2/results",result_publish,hostname=collector_address)

    else:
        
        try:
            push_to_drive(source_path_stem, now, destination_path_stem)
            
        except:
            print("failed to write to drive! check status of mount and refresh the token using rclone config")
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger2_address, 1883, 60)

client.loop_forever()
