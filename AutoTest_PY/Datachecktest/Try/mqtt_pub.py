# encoding: utf-8

import paho.mqtt.client as mqtt
import datetime
import json
import random
import time

HOST = "172.16.3.18"
PORT = 1883
timeslmp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')

data ={
	"p": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"p_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"t": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"t_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"bp": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"bp_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"so2": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"so2_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"bat": 0,
	"rssi": 0,
	"sos_state": 'false',
	"p": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"p_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"t": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"t_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"bp": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"bp_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"so2": "[231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000, 231.1000]",
	"so2_time": "[12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346, 12346]",
	"bat": 0,
	"rssi": 0,
}

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    if mid == 0:
        print('推送失败，mid:%d'%mid)

def on_message(client, userdata, msg):
    print('主题:'+msg.topic+" "+'消息:'+str(msg.payload.decode('utf-8')))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)

def pub():
    # param=json.dumps(data)
    client = mqtt.Client()
    # client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect("172.16.3.18", 1883, 100)
    client.subscribe('mqtt/test',qos=1)
    time.sleep(5)
    print('++++++++++++')
    for i in range(25):
        # client.on_publish = on_publish
        client.publish('mqtt/test',payload='HELLO,小胖,东哥'+str(i),qos=1)
        # client.loop_start()

    client.loop_forever()


pub()