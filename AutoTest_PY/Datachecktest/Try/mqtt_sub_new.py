#!/usr/bin/python3

import queue
import json
import threading
import random
from time import *
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

threadLock = threading.Lock()
threads = []
data_gps ={
	"header":"B9YFH6PPOM$9999$01",
    "data":{
        "0": [[118.966205,30.638575,540000,60],[118.966205,30.638575,540000,120]],
		"10":1561781891
    }
}

data_sos ={
	"header":"B9YFH6PPOM$9999$00",
    "data":{
    "0":0,
    "1":{
        "0": [70,10],
        "1": [37.5,10],
        "10":1553238814
        },
    "10":1553238814
    }
}

data = [data_gps,data_sos]

class myThread(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("Starting " + self.name)
      # 获得锁，成功获得锁定后返回True
      # 可选的timeout参数不填时将一直阻塞直到获得锁定
      # 否则超时后将返回False
      # threadLock.acquire()
      pub()
      # 释放锁
      # threadLock.release()

def print_time(threadName, delay, counter):
   while counter:
        print(delay)
        time.sleep(delay)
      # print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def pub():
    for i in range(1000):
        param=json.dumps(random.choice(data))
        time.sleep(random.randint(15,38))
        publish.single('mqtt/sub/test',payload=param+str(i),qos=1,hostname="172.16.3.11",port=1883)
        print(i)

# 创建新线程
for counter in range(1):
    t = myThread(1, "Thread-"+str(counter), 1)
    threads.append(t)
# 开启新线程
for t in threads:
    sleep(0.3)
    t.start()
# 等待所有线程完成
for t in threads:
   t.join()
print ("退出主线程")
