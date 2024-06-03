#code that will be responsible for handling networking on the logger3 side of things

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import pyvisa as visa
from hat_methods import get_potential_difference
from peak_finding import get_var

#from datetime import date
import datetime

from spreadsheet_managing import write_locally, push_to_drive

#for our purposes, we'll call this Pi logger3, which will be in charge of all the 780 lasers' lock statuses

resources = visa.ResourceManager("@py")
print(resources.list_resources())

#need to confirm this before running
rigol = resources.open_resource('USB0::6833::1200::DS2D193902418::0::INSTR')

collector_address = "192.168.0.194"
logger3_address = "192.168.0.185"

status_count = [0,0,0]

fields = ['Time','780 Master Status', '780 Cooling Status', '780 Repump Status']
source_path_stem = r'/media/rbyb/C490-B476/'
#header_flag = True

header_flag = True
path = ""
now = datetime.date.today()

destination_path_stem = r'/home/rbyb/mnt/gdrive/Lab Monitoring System/Rb MOT Pi/'

#then, we need to subscribe it to something called "logger1/inquiries"
#so, this Pi will be listening for the master pi to request logger1 measurements

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger3/inquiries")
    client.subscribe("publish_requests")
    
def on_message(client, userdata, msg):
    
    global header_flag
    global now
    
    print(msg.topic+" "+str(msg.payload))
    
    payload = msg.payload.decode("utf-8")
    
    if payload == "data please <3":
    
        try:
            m_status = get_var(rigol, 300)
                
        except:
            print("failed to read 780 master lock status :()")
            m_status = 9999
        
        try:
            #put the cooling lock signal on AIO0 and AIO1 on the DAQ-HAT
            c_status = get_potential_difference(0,1)
            
        except:
            print("failed to read 780 cooling lock status :(")
            c_status = 9999
            
        try:
            #put the repump lock signal on AIO2 and AIO3 on the DAQ-HAT
            r_status = get_potential_difference(2,3)
            
        except:
            print("failed to read 780 repump lock status :(")
            r_status = 9999
        
        #maintaining for testing
        
        '''m_status = 1e-11
        c_status = random.randrange(1)
        r_status = random.randrange(2)'''
        
        now = datetime.date.today()
        time = datetime.datetime.now()
        stime = time.strftime("%c")
        
        result_return = [{'Time': stime, '780 Master Status': m_status, '780 Cooling Status': c_status, '780 Repump Status': r_status}]

        #write to spreadsheet
        #header_flag, path, now = write_locally(result_return, fields, source_path_stem, header_flag)
        write_locally(result_return, fields, source_path_stem, header_flag)
        
        header_flag = False
        
        print("written locally!")
        
        
        #write to collector
        #publish.single("logger3/results", {'780 Master Status': m_status, '780 Cooling Status': c_status, '780 Repump Status': r_status}, hostname=collector_address)

    else:
        push_to_drive(source_path_stem, now, destination_path_stem)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger3_address, 1883, 60)

client.loop_forever()
