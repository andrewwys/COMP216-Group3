# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:30:11 2022
@author: COMP216 Assignment 5 - Group 3
group_3_publisher.py
"""

import group_3_util
import json
import paho.mqtt.client as mqtt
import time

broker = "mqtt.eclipseprojects.io"

client = mqtt.Client()

print("connecting to Broker", broker)

client.connect(broker, 1883)

client.loop_start()

while True:
    mydict = group_3_util.create_data()
    dict_str = json.dumps(mydict)
    client.publish("indoorTemp", payload=dict_str)
    print('Just published' + str(dict_str) + 'to topic indoorTemp')
    time.sleep(2)

client.loop_stop()
client.disconnect()