#!usr/bin/env python
# encoding:utf-8

from configobj import ConfigObj
import  requests
import os
import codecs
import configparser
import json
import ast
from collections import Counter
import sys
from time import *
import threading
from Common import Read_config
from Common import Loging
import pymysql

cf=Read_config.ReadConfig()


def muisc(func):
    for i in range(2):
        # print('Start playing： %s! %s' %(func,ctime()))
        sleep(2)

def move(func):
    for i in range(2):
        # print('Start playing： %s! %s' %(func,ctime()))
        sleep(3)

def player(name):
    r= name.split('.')[1]
    if r=='mp3':
        muisc(name)
    elif r=='mp4':
        move(name)
    else:
        print('error')

list= ['爱情买卖.mp3','阿凡达.mp4']

threads=[]
files=range(len(list))

for i in files:
    t= threading.Thread(target=player,args=(list[i],))
    print(t)
    threads.append(t)

# print(threads)
if __name__ == '__main__':
#启动线程
    # for i in files:
    #     threads[i].start()
    # for i in files:
    #     threads[i].join()
    for i in threads:
        i.start()
    for i in threads:
        i.join()

    print('%s'%ctime())

