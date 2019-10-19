#!usr/bin/env python
# encoding:utf-8

import pymysql
import requests
import json
import os
import configparser
import ast
import threading
from time import *
from collections import Counter
# from Common import Read_config
# from Common import Loging

#获取配置信息
# cf=Read_config.ReadConfig()
# timeout= float(cf.get_http('timeout'))
# token=(Loging.login_DZ()[0])


#接口请求推荐大学
channel_url='https://testmin.ubzyw.com/channel/v2/rest/channel/channelUserCountList?rows=999&page=1'
channel_data={'page':1,'rows':20,'UB_UserAgent_appUserAuthToken':'f54d846f6894d30d97186034f439998a'}
channel=requests.post(channel_url,data=channel_data)
channel_request=(channel.json())

print(channel_request)


#
channel=[]


def get_info_channel(i):
    if channel_request['data']['rows'][i]['userNum'] != 0:
        channel.append(channel_request['data']['rows'][i]['userNum'])
    else:
        return None

#获取返回条数
channel_request_str =str(channel_request)
rows =channel_request_str.count('name')

threads6=[]
for i in range(rows):
    t6= threading.Thread(target=get_info_channel,args=(i,))
    threads6.append(t6)

for i in threads6:
    i.start()
for i in threads6:
    i.join()

print(sum(channel))

