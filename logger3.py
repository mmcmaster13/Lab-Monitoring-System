#code that will be responsible for handling networking on the logger3 side of things

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import pyvisa as visa
import hat_methods import get_potential_difference
from peak_finding import get_var

#for our purposes, we'll call this Pi logger3, which will be in charge of all the 780 lasers' lock statuses

resources = visa.ResourceManager("@py")
print(resources.list_resources())

#need to confirm this before running
rigol = resources.open_resource('USB0::6833::1200::DS2D193902418::0::INSTR')

collector_address = "192.168.0.178"
logger3_address = ""

status_count = [0,0,0]

#then, we need to subscribe it to something called "logger1/inquiries"
#so, this Pi will be listening for the master pi to request logger1 measurements

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("logger3/inquiries")
    
def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    #it's really just not worth waiting around for these to read
    #if it's going to get resolved on its own, it will be resolved on the next iteration
    #else it's not going to get resolved even if we wait here
    
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
    
    #format the string; has to be a string, cannot be another variable (e.g. dictionary)
    #but we can make it emulate a dictionary by splitting key:value with colons and quadruplets with commas:
    #also for IFTTT purposes, we need to label each with a 'valuen' tag
    
    #so, the format for this is as follows: valuen:description:threshold:measured value
    
    result_return = "value4:780 Master Status:1E-9:" + str(m_status) + ",value5:780 Cooling Status:0.4:" + str(c_status) + ",value6:780 Repump Status:1.2:" + str(r_status)
    
    #write to collector
    
    publish.single("logger3/results", result_return, hostname=collector_address)
    
#initiate idle listener

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(logger3_address, 1883, 60)

client.loop_forever()