import pymysql
import requests
import json
import time
import os
import configparser
from Common import Read_config

cf=Read_config.ReadConfig()


#获取参数
host = cf.get_database('host')
root = cf.get_database('username')
pwd = cf.get_database('password')
db = cf.get_database('database')

DB = pymysql.connect(host,root,pwd,db)
#创建游标对象
cursor = DB.cursor()
user_id=[]

#查询user_id
sql_user_id='SELECT user_id FROM tab_user_info WHERE class_id in (1291,1292)'

1291,1292
cursor.execute(sql_user_id)
user_id_results = cursor.fetchall()
for (i,) in user_id_results:
    user_id.append(i)


#查询通知消息
sql_msg_title='SELECT title,summary,user_id from tab_sys_user_msg WHERE user_id= %s ORDER BY create_time DESC LIMIT 1'
title='想要看看您的本次成绩完全分析么'
msg='以帮助您更好的了解自己各学科所处位次与水平'
for userid in range(len(user_id)):
    cursor.execute(sql_msg_title,(user_id[userid]))
    msg_results = cursor.fetchall()
    print(msg_results)
    for i in msg_results:
        if i[0]=='':
            print('出现空的情况:%s++++%s++++%s'%(i[0],i[1],i[2]))
        elif i[0]!='3 x 考试成绩发布了，想要看看您的本次成绩完全分析么？':
            print('标题不正确:%s++++%s'%(i[0],i[2]))
        elif i[1]!='根据本次成绩，我们做了多维度的分析，以帮助您更好的了解自己各学科所处位次与水平。具体请点击按钮查看。':
            print('内容不正确:%s++++%s'%(i[1],i[2]))






