#!usr/bin/env python
# encoding:utf-8

import pymysql
import requests
import json
import time
import os
import configparser
import ast
from collections import Counter
from Common import Read_config
from Common import Loging


cf=Read_config.ReadConfig()
timeout= float(cf.get_http('timeout'))


#登录账号/获取token
token=(Loging.login_3_3()[0])

#接口请求获取考试id
getLastExam_url='http://api.ubzyw.com/v1/rest/studentaim/getLastExam'
getLastExam_content={'UB_UserAgent_appUserAuthToken':token}
getLastExam=requests.get(getLastExam_url,params=getLastExam_content)


getLastExam_request=(getLastExam.json())
examId = getLastExam_request['data']['examId']

#接口请求3+3目标推荐页面

getAimRecommendSchoolList2_url='http://api.ubzyw.com/v1/rest/studentaim/getAimRecommendSchoolList2'
getAimRecommendSchoolList2_content={'addScore':10,'examId':examId,'subjectGroupId':15,'totalNum':50,'UB_UserAgent_appUserAuthToken':token}
getAimRecommendSchoolList2=requests.get(getAimRecommendSchoolList2_url,params=getAimRecommendSchoolList2_content)
getAimRecommendSchoolList2_request=(getAimRecommendSchoolList2.json())


#定义列表
#小类
getAimRecommendSchoolList2_schoolId=[]
getAimRecommendSchoolList2_schoolMajorId=[]
getAimRecommendSchoolList2_subject=[]


#大类
get_schoolAdmissionId=[]
get_schoolAdmissionId_subject=[]

#接口返回数据中取出大类id,组合；小类id,科目组合,学校id
i=0
getAimRecommendSchoolList2_request_str =str(getAimRecommendSchoolList2_request)
rows =getAimRecommendSchoolList2_request_str.count('schoolName')
while i <rows :
    if getAimRecommendSchoolList2_request['data'][i]['schoolAdmissionId'] == None:
        getAimRecommend_majorSubjectList=(getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'])
        getAimRecommend_majorSubjectList_str =str(getAimRecommend_majorSubjectList)
        count=getAimRecommend_majorSubjectList_str.count('title')
        x=0
        s=""
        while x <count:
            if(x==0):
                s=s+getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'][x]['title']
            else:
                s=s+","+getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'][x]['title']
            x+=1
        getAimRecommendSchoolList2_subject.append(s)
        getAimRecommendSchoolList2_schoolId.append(getAimRecommendSchoolList2_request['data'][i]['schoolId'])
        getAimRecommendSchoolList2_schoolMajorId.append(getAimRecommendSchoolList2_request['data'][i]['schoolMajorId'])
    else:
        get_schoolAdmissionId.append(getAimRecommendSchoolList2_request['data'][i]['schoolAdmissionId'])
        getAimRecommend_majorSubjectList=(getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'])
        getAimRecommend_majorSubjectList_str =str(getAimRecommend_majorSubjectList)
        count=getAimRecommend_majorSubjectList_str.count('title')
        x=0
        s=""
        while x <count:
            if(x==0):
                s=s+getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'][x]['title']
            else:
                s=s+","+getAimRecommendSchoolList2_request['data'][i]['majorSubjectList'][x]['title']
            x+=1
        get_schoolAdmissionId_subject.append(s)

    i+=1


print('小类专业组合%s' %(getAimRecommendSchoolList2_subject))
# print(getAimRecommendSchoolList2_schoolId)
# print(getAimRecommendSchoolList2_schoolMajorId)
print('大类专业组合%s'%(get_schoolAdmissionId_subject))
# print(get_schoolAdmissionId)


#接口请求获取具体小类专业组合信息
schoolMajorInfo_url='http://api.ubzyw.com/v1/rest/school/schoolMajorInfo'

schoolMajorInfo_list=[]

for i in range(len(getAimRecommendSchoolList2_schoolId)):
    schoolMajorInfo_content={'schoolId':getAimRecommendSchoolList2_schoolId[i],'schoolMajorId':getAimRecommendSchoolList2_schoolMajorId[i],'UB_UserAgent_appUserAuthToken':token}
    schoolMajorInfo=requests.get(schoolMajorInfo_url,params=schoolMajorInfo_content,timeout=timeout)
    schoolMajorInfo_request=(schoolMajorInfo.json())
    schoolMajorInfo_list.append(schoolMajorInfo_request['data']['subject'])

# print(schoolMajorInfo_list)

for i in range(len(getAimRecommendSchoolList2_subject)):
        if getAimRecommendSchoolList2_subject[i] == schoolMajorInfo_list[i]:
            continue
        print('组合不匹配数据:%s,%s,%s,%s'%(getAimRecommendSchoolList2_schoolId[i],getAimRecommendSchoolList2_schoolMajorId[i],getAimRecommendSchoolList2_subject[i],schoolMajorInfo_list[i]))
else:
    print('小类对比完成')





#接口请求获取具体大类专业组合信息

getSchoolAdmission_url='http://api.ubzyw.com/v1/rest/schoolAdminssion/getSchoolAdmission'

getSchoolAdmission_list=[]

for i in range(len(get_schoolAdmissionId)):
    getSchoolAdmission_content={'schoolAdmissionId':get_schoolAdmissionId[i],'UB_UserAgent_appUserAuthToken':token}
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

for i in range(len(get_schoolAdmissionId_subject)):
        if get_schoolAdmissionId_subject[i] == getSchoolAdmission_list[i]:
            continue
        print('组合不匹配数据:%s,%s,%s'%(get_schoolAdmissionId[i],get_schoolAdmissionId_subject[i],getSchoolAdmission_list[i]))
else:
    print('大类对比完成')