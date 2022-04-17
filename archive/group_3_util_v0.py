# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:16:06 2022

@author: User
"""

import random
import time
import math

#util.py

# Create wind speed data
def create_data():

    noise = random.randint(-100,100) / 500
    timestamp = time.asctime()
    x = (int(timestamp[-7:-5]) / 7.5) -4  # generate a number from -4 to 4 
    y = math.sin(x) * 1.5 + 18 + noise

    data_point = {
        "timeCreated": timestamp,
        "temperature": y
    }    
    return data_point
