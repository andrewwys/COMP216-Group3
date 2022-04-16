# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:30:11 2022

@author: User
"""

import group_3_util
import json
import paho.mqtt.client as mqtt
import time

#Publisher.py

for i in range(5):
    mydict = group_3_util.create_data()
    dict_str = json.dumps(mydict)
    
    client_name = "client-sub"
    broker = "mqtt.eclipseprojects.io"
    
    client = mqtt.Client(client_name)
    
    print("connecting to Broker", broker)
    
    client.connect(broker)
    
    time.sleep(4)
    
    print('Just published' + str(dict_str) + 'to topic studentdata')
    client.disconnect()