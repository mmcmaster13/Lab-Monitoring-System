import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import requests
import time

from Pi import Pi

from do_checks_networking_version import do_checks

#this is going to have to be modified at the addition of each Pi but won't need to be touched again
#probably should set up static IPs
logger1 = Pi("logger1", "192.168.0.185")

pis = [logger1]

ifttt_data = {}
labeled_data = {}
thresholds = {}

crit_counts = {}

reply = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    #client.subscribe("logger1/results")
 
    #subscribing to the results topic for each Pi
    for pi in pis:
        topic = pi.name + "/results"
        client.subscribe(topic)
    
def on_message(client, userdata, msg):
    
    global reply
    
    reply = msg.payload.decode()
    
    quads = reply.split(',')
    
    print("reply: " , reply)
    
    #taking triplets apart to create dictionary for IFTTT
    
    for quad in quads:
        quad_split = quad.split(':')
        ifttt_data[quad_split[0]] = float(quad_split[3])
        
        labeled_data[quad_split[1]] = float(quad_split[3])
        thresholds[quad_split[1]] = float(quad_split[2])
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#we want to read off data sent to this machine, so the client IP address should
#be the one for the collector (184)
client.connect("192.168.0.184", 1883, 60)

client.loop_start()

while True:
    
    try:
        
        for pi in pis:
            #we want to write to the measurer so the hostname needs to be its IP (185)
            topic = pi.name + "/inquiries"
            publish.single(topic, "data please <3", hostname = "192.168.0.185")
            print("data requested")
            
            #wait for reply (measurement timeout will be taken care of by measurers)
            while len(reply) == 0:
                time.sleep(0.1)
            
            #pause so everything can be settled before writing to IFTTT
            time.sleep(10)
            
        #do_checks to make sure no one is out of line; manage discord messaging
        #updates crit_counts
        crit_counts = do_checks(labeled_data, thresholds, crit_counts)
        
        #write to IFTTT
        print("IFTTT data: " , ifttt_data)
        
        r = requests.post("https://maker.ifttt.com/trigger/data_collected/with/key/cp5kerGL75CjAK7YNML9Zp", data=ifttt_data)

        reply = ""

        time.sleep(60)

    except requests.exceptions.HTTPError as errh: 
        print("HTTP Error")
        print(errh.args[0])
        print("occurred at: " + date_time)
      
    except requests.exceptions.ReadTimeout as errrt: 
        print("Time out")
        print("occurred at: " + date_time)
      
    except requests.exceptions.ConnectionError as conerr: 
        print("Connection error")
        print("occurred at: " + date_time)
