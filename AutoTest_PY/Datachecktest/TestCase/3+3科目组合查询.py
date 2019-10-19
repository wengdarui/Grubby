#!usr/bin/env python
# encoding:utf-8

import pymysql
import requests
import json
import time
from collections import Counter

login_url='http://testapi.ubzyw.com/v1/rest/login/doLogin'
login_content={'password':123456,'phoneOrEmail':18888000010}
login_header={'UB_UserAgent_deviceOS':'ios'}
login=requests.get(login_url,params=login_content,headers=login_header)

request=(login.json())
token=(request.get('data').get('token'))



getUserAim_url='http://testapi.ubzyw.com/v1/rest/studentaim/getUserAim2'
getUserAim_content={'coverageFlag':1,'groupId':4,'UB_UserAgent_appUserAuthToken':token}
getUserAim=requests.get(getUserAim_url,params=getUserAim_content)

getUserAim_request=(getUserAim.json())


subjects_id=(getUserAim_request['data']['list'])

if subjects_id:
    subjects=(getUserAim_request['data']['list'][0]['subjectGroupName'])
    subjectGroupId=(getUserAim_request['data']['list'][0]['subjectGroupId'])
else:
    subjects='物政历'
    subjectGroupId=4

print(subjects)
print(subjectGroupId)

db = pymysql.connect('rm-bp1hsp7r0cq8736ew1o.mysql.rds.aliyuncs.com','admin_root','JeeM21uoD2tBXpTu','ub_zy')

#创建游标对象
cursor = db.cursor()
#查询科目组合
cursor.execute('SELECT a.subject_id FROM tab_r_group_subject a LEFT JOIN tab_subject_group b ON a.subject_group_id=b.ID WHERE b.title=%s',(subjects))
subject_group=[]
results_kemu = cursor.fetchall()
result=list(results_kemu)
for i in result:
    subject_group.append(i[0])


#去除默认语数外组合id
subject_groupid=[]
default_id = [1,2,3]

for id in subject_group:
    if id not in default_id:
        subject_groupid.append(id)


#转换list int -》 str
# subjectstr=[ str(i) for i in subject_groupid ]
# subject_str=",".join(subjectstr)
# print(type(subject_str))
# print(subject_str)


#查询可报考专业

zy_result=[]
cursor.scroll(0,mode='absolute')
for x in subject_groupid:
    cursor.execute('SELECT school_major_id,year FROM tab_school_major_subject WHERE subject_id =(%s) AND sel_flag in(0,1) AND province_id=22 AND year=(SELECT MAX(year) from tab_school_major_subject WHERE province_id=22)',(x))
    result = cursor.fetchall()
    result_ZY=list(result)
    for i in result_ZY:
        zy_result.append(i[0])

# print(zy_result)

#专业id 去重
zy_result_set=list(set(zy_result))


#专业id 划分大类小类
Xmajor_id=[]
cursor.scroll(0,mode='absolute')
cursor.execute('SELECT DISTINCT school_major_id,major_title FROM tab_score_major_id')
result = cursor.fetchall()
result_Xmajor=list(result)
for i in result_Xmajor:
    Xmajor_id.append(i[0])


Dmajor_id=[]
cursor.scroll(0,mode='absolute')
cursor.execute('SELECT DISTINCT school_major_id,school_admission_id FROM tab_school_admission_major')
result = cursor.fetchall()
result_Dmajor=list(result)
for i in result_Dmajor:
    Dmajor_id.append(i[0])


Dmajor_list=list(set(zy_result_set).intersection(set(Dmajor_id)))
Xmajor_list=list(set(zy_result_set).intersection(set(Xmajor_id)))

# print(len(Dmajor_list))


Xmajor_str=[ str(i) for i in Xmajor_list ]
Xmajor_new_list=','.join(Xmajor_str)

Dmajor_str=[ str(i) for i in Dmajor_list ]
Dmajor_new_list=','.join(Dmajor_str)


# print(type(Xmajor_new_list))
# print(Xmajor_new_list)



#查询考试成绩
phone=18888000010
cursor.scroll(0,mode='absolute')
sql_fengshu='''SELECT t2.hexam_score FROM tab_user t1 LEFT JOIN tab_exam_total_score2 t2 ON t1.id = t2.user_id LEFT JOIN tab_exam t3 ON t2.exam_id = t3.id
                WHERE t3.stat_flag = 1 AND t3.subject_id = 0 AND t1.phone = %s AND t2.subject_group_id=%s ORDER BY t3.start_date DESC LIMIT 1 '''

cursor.execute(sql_fengshu,(phone,subjectGroupId))

hexam_score_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    hexam_score_list.append(i[0])
hexam_score=hexam_score_list

print(hexam_score)

hexam_score_str=[ str(i) for i in hexam_score ]
hexam_score_new=''.join(hexam_score_str)


#通过分数过滤查询可以报考的专业

# 小类专业id
sql_zhuanye_subclass='SELECT t1.school_id,t1.school_batch_id FROM `tab_score_major` t1 LEFT JOIN tab_score_major_id t2 ON t1.id=t2.score_major_id WHERE t2.school_major_id in({0}) AND t1.del_flag=0 AND t1.score<={1} AND t1.student_province_id =22 GROUP BY t1.school_id'.format(Xmajor_new_list,hexam_score_new)

#大类专业id
sql_zhuanye_bigclass='SELECT t1.school_id,t1.`year` FROM `tab_school_admission` t1 LEFT JOIN tab_school_admission_major t2 ON t1.id=t2.school_admission_id LEFT JOIN tab_school_admission_score t3 ON t2.school_admission_id=t3.school_admission_id WHERE t2.school_major_id in({0}) AND t1.del_flag=0  AND t3.score <={1} AND t1.student_province_id =22 GROUP BY t1.school_id'.format(Dmajor_new_list,hexam_score_new)



schoolId_list_subclass=[]
schoolBatchId_list_subclass=[]
cursor.scroll(0,mode='absolute')

cursor.execute(sql_zhuanye_subclass)
result = cursor.fetchall()
result_fs=list(result)
for i in result_fs:
    schoolId_list_subclass.append(i[0])
    schoolBatchId_list_subclass.append(i[1])

print(len(schoolId_list_subclass))

schoolId_list_bigclass=[]
schoolBatchId_list_bigclass=[]
cursor.scroll(0,mode='absolute')

cursor.execute(sql_zhuanye_bigclass)
result = cursor.fetchall()
result_fs=list(result)
for i in result_fs:
    schoolId_list_bigclass.append(i[0])

print(len(schoolId_list_bigclass))

schoolId_list_all= list(set(schoolId_list_subclass).union(set(schoolId_list_bigclass)))
schoolId_list_all=set(schoolId_list_all)


print(len(schoolId_list_all))
print(schoolId_list_all)


#查询双一流大学

cursor.scroll(0,mode='absolute')
cursor.execute('SELECT school_id from tab_school_property where school_property_id  = 17 GROUP BY school_id')

schoolId17_list=[]
results = cursor.fetchall()
result=list(results)
for i in result:
    schoolId17_list.append(i[0])

# 能报考的双一流大学
school_two1=list(set(schoolId_list_all).intersection(set(schoolId17_list)))
print('数量%d'%len(school_two1),'预期能报考的双一流大学:%s'% school_two1)








db.close()