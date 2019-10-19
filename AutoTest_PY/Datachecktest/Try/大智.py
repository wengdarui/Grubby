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
from Common import Read_config
from Common import Loging

#获取配置信息
cf=Read_config.ReadConfig()
timeout= float(cf.get_http('timeout'))
token=(Loging.login_DZ()[0])


#接口请求推荐大学
recommend_url='https://min.ubzyw.com/school/v1/rest/recommend/school'
recommend_data={'page':1,'rows':999,'batchId':6,'UB_UserAgent_appUserAuthToken':token}
recommend6=requests.post(recommend_url,data=recommend_data)
recommend6_request=(recommend6.json())


recommend_url='https://min.ubzyw.com/school/v1/rest/recommend/school'
recommend_data={'page':1,'rows':999,'batchId':7,'UB_UserAgent_appUserAuthToken':token}
recommend7=requests.post(recommend_url,data=recommend_data)
recommend7_request=(recommend7.json())

recommend_url='https://min.ubzyw.com/school/v1/rest/recommend/school'
recommend_data={'page':1,'rows':999,'batchId':354,'UB_UserAgent_appUserAuthToken':token}
recommend354=requests.post(recommend_url,data=recommend_data)
recommend354_request=(recommend354.json())



#定义列表
#大类
schoolName6=[]
schoolName7=[]
schoolName354=[]

#获取返回条数
recommend6_request_str =str(recommend6_request)
rows6 =recommend6_request_str.count('schoolName')

recommend7_request_str =str(recommend7_request)
rows7 =recommend7_request_str.count('schoolName')

recommend354_request_str =str(recommend354_request)
rows354 =recommend354_request_str.count('schoolName')



#接口返回数据中取出大类id,组合；小类id,科目组合,学校id

def get_info6(i):
    if recommend6_request['data']['rows'][i]['admissionNum'] == 0:
        schoolName6.append(recommend6_request['data']['rows'][i]['schoolName'])
        schoolName6.append(recommend6_request['data']['rows'][i]['schoolId'])


    else:
        return None
def get_info7(i):
    if recommend7_request['data']['rows'][i]['admissionNum'] == 0:
        schoolName7.append(recommend7_request['data']['rows'][i]['schoolName'])
        schoolName7.append(recommend7_request['data']['rows'][i]['schoolId'])


    else:
        return None
def get_info354(i):
    if recommend354_request['data']['rows'][i]['admissionNum'] == 0:
        schoolName354.append(recommend354_request['data']['rows'][i]['schoolName'])
        schoolName354.append(recommend354_request['data']['rows'][i]['schoolId'])


    else:
        return None

threads6=[]
threads7=[]
threads354=[]
for i in range(rows6):
    t6= threading.Thread(target=get_info6,args=(i,))
    threads6.append(t6)

for i in threads6:
    i.start()
for i in threads6:
    i.join()

for i in range(rows7):
    t7= threading.Thread(target=get_info7,args=(i,))
    threads7.append(t7)

for i in threads7:
    i.start()
for i in threads7:
    i.join()


for i in range(rows354):
    t354= threading.Thread(target=get_info354,args=(i,))
    threads354.append(t354)

for i in threads354:
    i.start()
for i in threads354:
    i.join()


print('一批次推荐专业为空的学校%s' %schoolName6)
print('二批次推荐专业为空的学校%s' %schoolName7)
print('专科批次推荐专业为空的学校%s' %schoolName354)

