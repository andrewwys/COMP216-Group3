# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:29:32 2022
@author: COMP216 Assignment 5 - Group 3
group_3_subscriber.py
"""
import paho.mqtt.client as mqtt
import json
import time
import threading
from tkinter import Tk, Canvas, Frame, BOTH, W, Button, Label

# Subscriber.py    

# using open source broker
broker = "mqtt.eclipseprojects.io"
# create client
client = mqtt.Client()

POINT_COUNT = 40
data_queue = []  # to store the received data

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# decode and print the message when received
def on_message (client, userdata, message):
    data = message.payload.decode("utf-8")
    obj = json.loads(data)
    updated_time = obj["timestamp"]
    data_queue.append(obj["temperature"]) # append new data to the queue
    print('message received: ', updated_time, data_queue[-1]) 
    print("data_queue: ", data_queue)
    if(len(data_queue) >= POINT_COUNT):   # if data is full, pop the first one
        data_queue.pop(0)

def start_client():
    client.on_message = on_message
    # connect to broker
    client.connect(broker, 1883)
    client.subscribe('indoorTemp')
    print('Subscribing')
    time.sleep(2)
    # client.loop_forever()
    client.loop_start()   # use loop_start() to start a new thread
    
    
# GUI Display
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 400
LINE_WIDTH = 2
LINE_SIZE = (GRAPH_WIDTH-50) / POINT_COUNT

class Dynamic_Display(Frame):
    
    lines = []
    
    def __init__(self):
        super().__init__()        
        # self.is_stopped = True
        self.initUI()
        self.update()    
       
    def initUI(self):
        self.master.title('Assignment 5 - Group 3')
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, bg='#FFF8B3')
        self.canvas.create_text(30, 30, anchor=W, font='Arial', text='Indoor Temperature Monitor')
        
        # draw the graph lines and measurements
        # x & y axis
        self.canvas.create_line(25 - LINE_WIDTH/2, 20, 25 - LINE_WIDTH/2, GRAPH_HEIGHT) 
        self.canvas.create_line(25 - LINE_WIDTH/2, GRAPH_HEIGHT, GRAPH_WIDTH + 25, GRAPH_HEIGHT) 
        # measurement labels
        Label(text='16`C', bg='#FFF8B3', font=('Arial',10)).place(x=GRAPH_WIDTH-30, y=GRAPH_HEIGHT-22) 
        Label(text='17`C', bg='#FFF8B3', font=('Arial',10)).place(x=GRAPH_WIDTH-30, y=GRAPH_HEIGHT-110)
        Label(text='18`C', bg='#FFF8B3', font=('Arial',10)).place(x=GRAPH_WIDTH-30, y=GRAPH_HEIGHT-200)
        Label(text='19`C', bg='#FFF8B3', font=('Arial',10)).place(x=GRAPH_WIDTH-30, y=GRAPH_HEIGHT-290)
        Label(text='20`C', bg='#FFF8B3', font=('Arial',10)).place(x=GRAPH_WIDTH-30, y=GRAPH_HEIGHT-380)
        # guiding lines
        self.canvas.create_line(25, GRAPH_HEIGHT-90, GRAPH_WIDTH-35, GRAPH_HEIGHT-90, fill='#cfcfcf')
        self.canvas.create_line(25, GRAPH_HEIGHT-180, GRAPH_WIDTH-35, GRAPH_HEIGHT-180, fill='#cfcfcf')
        self.canvas.create_line(25, GRAPH_HEIGHT-270, GRAPH_WIDTH-35, GRAPH_HEIGHT-270, fill='#cfcfcf')
        self.canvas.create_line(280, GRAPH_HEIGHT-360, GRAPH_WIDTH-35, GRAPH_HEIGHT-360, fill='#cfcfcf')
        
        # initialize the data lines
        for i in range(POINT_COUNT):
            self.lines.append(self.canvas.create_line(0,0,0,0,fill='#184c8f', width=2))
        self.canvas.pack(fill=BOTH, expand=1) 
        self.update()
        
        # start button
        start_button = Button(text='Start', width=20, command=lambda:self.startBtn())
        start_button.place(x=GRAPH_WIDTH-450, y=GRAPH_HEIGHT+35)
        
    # redraw the lines with values in data_queue   
    def value_change(self):
        while True:
            for i, line in enumerate(self.lines):
                if (i >= len(data_queue)-1):
                    break
                else:
                    # this is the y coordinates of point i and i+1
                    # *90 is a scale to match the measurement guiding lines
                    y1 = GRAPH_HEIGHT - (data_queue[i] - 16) * 90  
                    y2 = GRAPH_HEIGHT - (data_queue[i+1] - 16) *90
                    self.canvas.coords(line, 25+(i+1)*LINE_SIZE, y2, 25+i*LINE_SIZE, y1)
            # print(data_queue[POINT_COUNT-1])
            self.update()
            time.sleep(2)
        
    def startBtn(self):
        start = threading.Thread(target=self.value_change())
        start.setDaemon(True)

    def on_closing(self):
        self.master.destroy()


if __name__ == "__main__":
    start_client()
    root = Tk()
    display = Dynamic_Display()
    root.geometry(f'{GRAPH_WIDTH+50}x{GRAPH_HEIGHT+100}+300+300')
    root.protocol("WM_DELETE_WINDOW", display.on_closing)
    root.mainloop()
    
    
    