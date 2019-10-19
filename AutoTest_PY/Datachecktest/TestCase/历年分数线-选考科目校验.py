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
token=(Loging.login_3_3()[0])


#接口请求获取历年分数线
yearScoreLine_url='http://api.ubzyw.com/v1/rest/yearScoreLine/new/list'
yearScoreLine_content={'page':1,'rows':999,'year':2017,'UB_UserAgent_appUserAuthToken':token}
yearScoreLine=requests.get(yearScoreLine_url,params=yearScoreLine_content)

yearScoreLine_request=(yearScoreLine.json())

#定义列表
#小类
yearScoreLine_schoolId=[]
yearScoreLine_schoolMajorId=[]
yearScoreLine_subject=[]

#大类
yearScoreLine_schoolAdmissionId=[]
yearScoreLine_schoolAdmissionId_subject=[]

yearScoreLine_request_str =str(yearScoreLine_request)
rows =yearScoreLine_request_str.count('schoolName')

#接口返回数据中取出大类id,组合；小类id,科目组合,学校id

def get_info(i):
    if yearScoreLine_request['data']['rows'][i]['schoolMajorId'] == None:
        yearScoreLine_schoolAdmissionId.append(yearScoreLine_request['data']['rows'][i]['schoolAdmissionId'])
        yearScoreLine_schoolAdmissionId_subject.append(yearScoreLine_request['data']['rows'][i]['subject'])

    else:
        yearScoreLine_schoolMajorId.append(yearScoreLine_request['data']['rows'][i]['schoolMajorId'])
        yearScoreLine_schoolId.append(yearScoreLine_request['data']['rows'][i]['schoolId'])
        yearScoreLine_subject.append(yearScoreLine_request['data']['rows'][i]['subject'])


# print('大类专业科目组合%s'%(yearScoreLine_schoolAdmissionId_subject))

threads=[]
for i in range(rows):
    t= threading.Thread(target=get_info,args=(i,))
    threads.append(t)

for i in threads:
    i.start()
for i in threads:
    i.join()



#接口请求获取具体小类专业组合信息
schoolMajorInfo_url='http://api.ubzyw.com/v1/rest/school/schoolMajorInfo'
schoolMajorInfo_list=[]
rows1=len(yearScoreLine_schoolId)


def get_schoolMajorInfo(Major):
    schoolMajorInfo_content={'schoolId':yearScoreLine_schoolId[Major],'schoolMajorId':yearScoreLine_schoolMajorId[Major],'UB_UserAgent_appUserAuthToken':token}
    schoolMajorInfo=requests.get(schoolMajorInfo_url,params=schoolMajorInfo_content,timeout=timeout)
    schoolMajorInfo_request=(schoolMajorInfo.json())
    schoolMajorInfo_list.append(schoolMajorInfo_request['data']['subject'])

print('%s'%ctime())
threads1=[]
for Major in range(rows1):
    t= threading.Thread(target=get_schoolMajorInfo,args=(Major,))
    threads1.append(t)

for t in threads1:
    sleep(0.2)
    t.start()
for t in threads1:
    sleep(0.2)
    t.join()

print('%s'%ctime())
print(schoolMajorInfo_list)

for i in range(len(yearScoreLine_subject)):
        if yearScoreLine_subject[i] == schoolMajorInfo_list[i]:
            continue
        print('组合不匹配数据（小类）++++学校id:%s,专业id:%s,外层:%s,里层:%s'%(yearScoreLine_schoolId[i],yearScoreLine_schoolMajorId[i],yearScoreLine_subject[i],schoolMajorInfo_list[i]))
else:
    print('小类对比完成')


#接口请求获取具体大类专业组合信息

getSchoolAdmission_url='http://api.ubzyw.com/v1/rest/schoolAdminssion/getSchoolAdmission'

getSchoolAdmission_list=[]

for i in range(len(yearScoreLine_schoolAdmissionId)):
    getSchoolAdmission_content={'schoolAdmissionId':yearScoreLine_schoolAdmissionId[i],'UB_UserAgent_appUserAuthToken':token}
    getSchoolAdmission=requests.get(getSchoolAdmission_url,params=getSchoolAdmission_content)
    getSchoolAdmission_request=(getSchoolAdmission.json())
    subjectTitle=(getSchoolAdmission_request['data']['subjectList'])
    subjectTitle_str =str(subjectTitle)
    list=subjectTitle_str.count('subjectTitle')
    x=0
    s=""
    while x <list:
        if(x==0):
            s=s+getSchoolAdmission_request['data']['subjectList'][x]['subjectTitle']
        else:
            s=s+","+getSchoolAdmission_request['data']['subjectList'][x]['subjectTitle']
        x+=1
    getSchoolAdmission_list.append(s)

print('大类专业详情组合%s'%(getSchoolAdmission_list))

for i in range(len(yearScoreLine_schoolAdmissionId_subject)):
        if yearScoreLine_schoolAdmissionId_subject[i] == getSchoolAdmission_list[i]:
            continue
        print('组合不匹配数据（大类）++++学校id:%s,专业id:%s,外层:%s,里层:%s'%(yearScoreLine_schoolAdmissionId[i],yearScoreLine_schoolAdmissionId_subject[i],getSchoolAdmission_list[i]))
else:
    print('大类对比完成')