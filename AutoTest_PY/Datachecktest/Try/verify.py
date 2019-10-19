#!usr/bin/env python
# encoding:utf-8

import time
import re
import pymysql
from collections import *

#
# def binary_search(num_list, x):
#     num_list=sorted(num_list)
#     left, right = 0, len(num_list)
#     while left < right:
#         mid = (left + right) // 2
#         if num_list[mid] > x:
#             right = mid
#         elif num_list[mid] < x:
#             left = mid + 1
#         else:
#             return '待查元素{0}在列表中下标为：{1}'.format(x, mid)
#     return  '待查找元素%s不存在指定列表中'%x
#
#
#
# if __name__ == '__main__':
#     num_list = [34,6,78,9,23,56,177,33,2,6,30,99,83,21,17]
#     print (binary_search(num_list, 34))
#


#获取参数
host = 'rm-bp122ilf6x2ihj8123o.mysql.rds.aliyuncs.com'
root = 'admin_root'
pwd = 'mu1E9hmGZOEWpgJ7'
db = 'tub_zy'


# host = '192.168.5.185'
# root = 'admin_api'
# pwd = 'U#*uxq2017gcz0s7'
# db = 'tub_zy'


DB = pymysql.connect(host,root,pwd,db,port=3306,charset='utf8')
#创建游标对象
cursor = DB.cursor()

#查询考试成绩
sql_fengshu='''SELECT `user` FROM `tab_common_test_report`  WHERE `del_flag`=0; '''

cursor.execute(sql_fengshu)

sc='北枳,舆杰,朱格,望川,甘扬'
yf='康德,佩奇,鲁班,路易,卓宸,章鹏,纽扣,猴子,威仔,奔驰,小熊,尼莫,野人,十七,文森,沉默,康俊	,谨谦,林宏,晓龙,康康,白丁,波波,天青,土豆,行知,华华,诺亚,小玄,小柚,小石,小胖,小庞,千峰,西泽,浩然,柠檬'
yw='文子,鱼子,滢子,简从,千曼,绿猪,篮子,邓子,言立,竹子,慕言,铃木,桔年,大李,特伦,肖恩'
pp='大卫,阿舟,威廉,言生,奎妮,薯条,花音,不眠,清风,林克,若鹏,小白,李易,冬妮,璐璐,萌酱,嘉芯,晏子,河马'
gx='天帅	,大田,小明,兴旺,龙泽,忆北,东皇,莉莉,小兴,岚君,森尼,,阿九,雪莉,井一,七言,九溪,女可,咸咸,冰心,十一,三秋,疯仔,泽文,江山'
zn='安可,球球,喜宝,亦雪,豆豆,白露'
cw='木兰,扬扬'
xs='乔特,天阔,容若,禾页'
od='欧德'

all=sc+yf+yw+pp+gx+zn+cw+xs+od

sc_list=[]
yf_list=[]
yw_list=[]
pp_list=[]
gx_list=[]
zn_list=[]
cw_list=[]
xs_list=[]
od_list=[]
weizhi_list=[]

results = cursor.fetchall()
result=list(results)
for i in result:
    if i[0] in sc:
        sc_list.append(i[0])
    if i[0] in yf:
        yf_list.append(i[0])
    if i[0] in yw:
        yw_list.append(i[0])
    if i[0] in pp:
        pp_list.append(i[0])
    if i[0] in gx:
        gx_list.append(i[0])
    if i[0] in zn:
        zn_list.append(i[0])
    if i[0] in cw:
        cw_list.append(i[0])
    if i[0] in xs:
        xs_list.append(i[0])
    if i[0] in od:
        od_list.append(i[0])
    elif i[0] not in all:
        weizhi_list.append(i[0])

print('提交问题总数%s'%len(result))
print('市场服务中心总数:%s---%s'%(len(sc_list),Counter(sc_list)))
print('研发中心总数:%s---%s'%(len(yf_list),Counter(yf_list)))
print('业务运营中心总数:%s---%s'%(len(yw_list),Counter(yw_list)))
print('品牌与产品运营中心总数:%s---%s'%(len(pp_list),Counter(pp_list)))
print('高校合作服务中心中心总数:%s---%s'%(len(gx_list),Counter(gx_list)))
print('职能服务中心中心总数:%s---%s'%(len(zn_list),Counter(zn_list)))
print('财务部总数:%s---%s'%(len(cw_list),Counter(cw_list)))
print('优彼学社总数:%s---%s'%(len(xs_list),Counter(xs_list)))
print('总经理总数:%s---%s'%(len(od_list),Counter(od_list)))
print('未匹配总数:%s---%s'%(len(weizhi_list),Counter(weizhi_list)))

