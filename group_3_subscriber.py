# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:29:32 2022

@author: User
"""
import paho.mqtt.client as mqtt
import json
import time
# import group_3_util

# Subscriber.py    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# decode and print the message when received
def on_message (client, userdata, message):
    print(message.topic+" "+str(message.payload))
    data = message.payload.decode("utf-8")
    obj = json.loads(data)
    print('message received ', obj["timeCreated"], obj["temperature"])
    # group_3_util.print_data(message)

# using open source broker
broker = "mqtt.eclipseprojects.io"

# create client
client = mqtt.Client()

client.on_message = on_message

# connect to broker
client.connect(broker, 1883)

client.subscribe('indoorTemp')
print('Subscribing')

time.sleep(2)

while True: 
    client.loop_forever()
