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
    param=json.dumps(data)
    for i in range(900):
        time.sleep(random.randint(120,180))
        id='tiger_dream_'+str(i)
        publish.single('DH/test/app',payload='++++++Websocket测试+++++第'+str(i)+'次',client_id="tiger_dream_0",qos=1,hostname="172.16.3.11",port=1883)
        print(i)

# 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

for counter in range(1):
    t = myThread(1, "Thread-"+str(counter), 1)
    threads.append(t)
# 开启新线程
# thread1.start()
# thread2.start()
for t in threads:
    sleep(0.5)
    t.start()
# 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)
# 等待所有线程完成
for t in threads:
   t.join()
print ("退出主线程")
