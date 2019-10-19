#!usr/bin/env python
# encoding:utf-8

import pymysql
import requests
import json
import time
import os
import configparser

proDir = os.path.split(os.path.realpath('E:\AutoTest_PY\Datachecktest\config.ini'))[0]
configpath = os.path.join(proDir,'config.ini')

#创建实例化对象
cf = configparser.ConfigParser()

#读取配置文件内容
cf.read(configpath,encoding='UTF8')
#获取参数
phone = cf.getint('HTTP','phone_3+x')
host = cf.get('DATABASE','host')
root = cf.get('DATABASE','username')
pwd = cf.get('DATABASE','password')
db = cf.get('DATABASE','database')
schoolId206_list = cf.get('schoolId','schoolId206_list')
schoolId207_list = cf.get('schoolId','schoolId207_list')



DB = pymysql.connect(host,root,pwd,db)
#创建游标对象
cursor = DB.cursor()

#查询考试成绩
sql_fengshu='''SELECT t2.hexam_score FROM tab_user t1 LEFT JOIN tab_exam_total_score t2 ON t1.id = t2.user_id LEFT JOIN tab_exam t3 ON t2.exam_id = t3.id
                WHERE t3.stat_flag = 1 AND t3.subject_id = 0 AND t1.phone = %s ORDER BY t3.start_date DESC LIMIT 1 '''

cursor.execute(sql_fengshu,(phone))

hexam_score_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    hexam_score_list.append(i[0])
hexam_score=hexam_score_list

#查询可以报考的大学
sql_daxue='''SELECT t1.score_school_id schoolId,t1.school_batch_id schoolBatchId from tab_score_info t1 where t1.student_province_id=22 and t1.arts_science=2 and t1.del_flag=0 and lowest_score<=%s
            and year=(SELECT MAX(year) from tab_score_info where del_flag  = 0 and score_school_id is not null)and t1.score_school_id is not null GROUP BY
	        t1.score_school_id'''

cursor.scroll(0,mode='absolute')
cursor.execute(sql_daxue,(hexam_score))

#获取学校id以及批次id
schoolId_list=[]
schoolBatchId_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    schoolId_list.append(i[0])
    schoolBatchId_list.append(i[1])

# print(Counter(schoolBatchId_list))
# print(len(set(schoolId_list)))

#查询双一流大学

# cursor.scroll(0,mode='absolute')
cursor.execute('SELECT school_id from tab_school_property where school_property_id  = 17 GROUP BY school_id')

schoolId17_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    schoolId17_list.append(i[0])


#查询一流大学
cursor.scroll(0,mode='absolute')
cursor.execute('SELECT school_id from tab_school_property where school_property_id  = 205 GROUP BY school_id')

schoolId205_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    schoolId205_list.append(i[0])

#关闭数据库连接
DB.close()

time.sleep(1)


#登录账号/获取token
login_url='http://testapi.ubzyw.com/v1/rest/login/doLogin'
login_content={'password':123456,'phoneOrEmail':13020000371}
login_header={'UB_UserAgent_deviceOS':'ios'}
login=requests.get(login_url,params=login_content,headers=login_header)


request=(login.json())
token=(request.get('data').get('token'))

#接口请求获取可报考大学
getUserAim_url='http://testapi.ubzyw.com/v1/rest/studentaim/getUserAim'
getUserAim_content={'coverageFlag':1,'groupId':4,'UB_UserAgent_appUserAuthToken':token}
getUserAim=requests.get(getUserAim_url,params=getUserAim_content)

getUserAim_request=(getUserAim.json())
request_schoolIds_two1=(getUserAim_request['data']['schoolNum'][0]['schoolIds'])
request_school_1=(getUserAim_request['data']['schoolNum'][1]['schoolIds'])
request_school_2=(getUserAim_request['data']['schoolNum'][2]['schoolIds'])
request_school_3=(getUserAim_request['data']['schoolNum'][3]['schoolIds'])

print(request_schoolIds_two1)
# 能报考的双一流大学
school_two1=list(set(schoolId_list).intersection(set(schoolId17_list)))
print('数量%d'%len(school_two1),'预期能报考的双一流大学:%s'% school_two1)


if request_schoolIds_two1 == '':
    print('实际双一流大学数量为0')
else:
    schoolIds_two1=request_schoolIds_two1.split(',')
    print('数量%d'%len(schoolIds_two1),'实际双一流大学：%s'%schoolIds_two1)


# 能报考的一流大学
school_1=list(set(schoolId_list).intersection(set(schoolId205_list)))
print('数量%d'%len(school_1),'预期能考的一流大学:%s'% school_1)

if request_school_1 == '':
    print('实际一流大学数量为0')
else:
    schoolIds_two1=request_school_1.split(',')
    print('数量%d'%len(schoolIds_two1),'实际一流大学：%s'%schoolIds_two1)


shuangyi_id=len(school_two1)
yi_id=len(school_1)


# 能报考的其余一本大学

school_2=0
if schoolBatchId_list == '':
    print('其余大学为空')
else:
    for i in schoolBatchId_list:
        for x in schoolId206_list:
            if i==x:
                school_2=school_2+1

    distinct_shuangyiid=school_2-shuangyi_id
    print('预期能考的其余一本大学数量%d'%distinct_shuangyiid)
    # print('批次%d出现次数%d'%(id,schoolBatchId_list.count(id)))

if request_school_2 == '':
    print('实际能考的其余一本大学数量为0')
else:
    schoolIds_two2=request_school_2.split(',')
    print('数量%d'%len(schoolIds_two2),'实际能考的其余一本大学：%s'%schoolIds_two2)



# 能报考的其余一本大学

school_3=0
if schoolBatchId_list == '':
    print('其余大学为空')
else:
    for i in schoolBatchId_list:
        for x in schoolId207_list:
            if i==x:
                school_3=school_3+1

    distinct_yiid=school_3-yi_id
    print('预期能考的其余本科大学数量%d'%distinct_yiid)


if request_school_3 == '':
    print('实际能考的其余本科大学数量为0')
else:
    schoolIds_two3=request_school_3.split(',')
    print('数量%d'%len(schoolIds_two3),'实际能考的其余本科大学：%s'%schoolIds_two3)
