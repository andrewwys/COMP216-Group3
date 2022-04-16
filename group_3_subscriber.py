# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:29:32 2022

@author: User
"""
import paho.mqtt.client as mqtt
import json
import time
import group_3_util

# Subscriber.py    

# decode and print the message when received
def on_message (client, userdata, message):
    string_message: str = message.payload.decode("utf-8")
    message = json.Loads(string_message)
    group_3_util.print_data(message)

# some client name
client_name = "client-sub"

# using open source broker
broker = "mqtt.eclipseprojects.io"

# create client
client = mqtt.Client(client_name)

# connect to broker
client.connect(broker)

print('Subscribing')
client.subscribe('studentdata')
client.on_message = on_message
time.sleep(2)

client.loop_forever()