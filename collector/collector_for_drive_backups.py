import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import requests
import time

import datetime

from Pi import Pi

#from do_checks_networking_version import do_checks

collector_address = "192.168.0.194"

#this is going to have to be modified at the addition of each Pi but won't need to be touched again
#probably should set up static IPs
logger1 = Pi("logger1", "192.168.0.193")
logger2 = Pi("logger2","192.168.0.197")
logger3 = Pi("logger3", "192.168.0.185")
logger4 = Pi("logger4","192.168.0.175")

pis = [logger1, logger2, logger3, logger4]

ifttt_data = {}
labeled_data = {}
thresholds = {}

crit_counts = {}

reply = ""
publish_count = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    #client.subscribe("logger1/results")
 
    #subscribing to the results topic for each Pi
    for pi in pis:
        topic = pi.name + "/results"
        client.subscribe(topic)
    
def on_message(client, userdata, msg):
    
    #push to InfluxDB eventually
    
    print("data received")
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#we want to read off data sent to this machine, so the client IP address should
#be the one for the collector (184)
client.connect(collector_address, 1883, 60)

client.loop_start()

while True:

    for pi in pis:

        topic = pi.name + "/inquiries"
        publish.single(topic, "data please <3", hostname = pi.address)
        print("data requested")
        
        #wait for reply (measurement timeout will be taken care of by measurers)
        while len(reply) == 0:
            time.sleep(0.1)
        
    #do_checks to make sure no one is out of line; manage discord messaging
    #updates crit_counts
        
    #temporarily commenting out this line because we don't care about Discord atm
    #crit_counts = do_checks(labeled_data, thresholds, crit_counts)
    
    reply = ""
    
    publish_count += 1
    
    if publish_count % 30 == 0:
        
        for pi in pis:
            topic = "publish_requests"
            publish.single(topic, "publish please <3", hostname = pi.address)
            print("publish requested")
            
        publish_count = 1

    time.sleep(60)