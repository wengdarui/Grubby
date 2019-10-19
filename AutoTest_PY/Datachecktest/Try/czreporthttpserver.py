#!/opt/python357/bin/python3
# -*- coding: utf-8 -*-
# __author:  千峰
# 修改竹子代码


import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from bottle import Bottle,run,response,request
import  bottle
import logging
import oss2
import datetime
import json


app = Bottle()
bottle.BaseRequest.MEMFILE_MAX=900000

@app.route('')
@app.route('/')
def showerror():
    return  '<h1> 错误请求，请重试!</h1>'

@app.route('/czpiccreate',method='post',encoding='UTF-8')
def czpiccreate():
    struse = request.forms.getunicode('scorejson')
    print(struse)
    #struse = eval(studentscore)
    # 初始数据处理
    editjsonuse = str.replace(str.replace(struse, 'subjectName', "科目"), 'score', "成绩")

    # 参数转字典
    diruse = eval(editjsonuse)

    stuexamId = diruse.get("examId")
    stuId = diruse.get("userId")
    stuscore = diruse.get("studentExam")

    # 主科学分
    gradeexamzk = str.replace(str(diruse.get("examzk")), '\'', '\"')
    gradeexamxk = str.replace(str(diruse.get("examxk")), '\'', '\"')
    gradeexamfxk = str.replace(str(diruse.get("examfxk")), '\'', '\"')

    # 科目列表
    # stuzklistuse = ['语文', '数学', '外语']
    stuzklist = diruse.get("zklist")
    stuxklist = diruse.get("xklist")
    stufxklist = diruse.get("fxklist")

    stuzklistuse = []
    for i in stuzklist.values():
        stuzklistuse.append(i)

    stuxklistuse = []
    for i in stuxklist.values():
        stuxklistuse.append(i)

    stufxklistuse = []
    for i in stufxklist.values():
        stufxklistuse.append(i)

    # 成绩列表
    # sutcoreusezk = []
    # sutcoreusezk.append(stuscore.get("yuwen"))
    # sutcoreusezk.append(stuscore.get("shuxue"))
    # sutcoreusezk.append(stuscore.get("waiyu"))
    sutcoreusezk = []
    for i in getkmlist(gradeexamzk, stuzklist):
        sutcoreusezk.append(stuscore.get(str.replace(str.replace(str.replace(str(i), '[', ''), ']', ''), '\'', '')))


    sutcoreusexk = []
    for i in getkmlist(gradeexamxk, stuxklist):
        sutcoreusexk.append(stuscore.get(str.replace(str.replace(str.replace(str(i), '[', ''), ']', ''), '\'', '')))

    sutcoreusefxk = []
    for i in getkmlist(gradeexamfxk, stufxklist):
        sutcoreusefxk.append(stuscore.get(str.replace(str.replace(str.replace(str(i), '[', ''), ']', ''), '\'', '')))

    # 正科生成图片
    url1= createpic(gradeexamzk, sutcoreusezk, stuzklistuse, stuexamId, stuId)
    # 选科生成图片
    url2= createpic(gradeexamxk, sutcoreusexk, stuxklistuse, stuexamId, stuId)
    # 非选课生成图片
    url3= createpic(gradeexamfxk, sutcoreusefxk, stufxklistuse, stuexamId, stuId)
    print(url1,url2,url3)
    return url1,url2,url3


@app.route('/czpiccreate')
def czpiccreate():
    print('++++++++')
    return  'request is get'


def ossuse(var):
    auth = oss2.Auth('LTAIT5MicSkqQBPx', '1fWKx1z1q8LoXanGXmpT7Vn78Zddx4')
    # 开启日志
    log_file_path = "log.log"
    oss2.set_file_logger(log_file_path, 'oss2', logging.INFO)
    bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'ubzy')
    upurl = r'/opt/xyfxreport/pic/%s' %var
    key = 'app/exam/exampic/%s'%var
    bucket.put_object_from_file(key, upurl)


def createpic(datasource, studentscore, choosekm, stuexamId, stuId):
    data1_1 = pd.read_json(datasource)

    # 构造数据源
    data1_1_2 = data1_1[['科目', '成绩']]

    #    print(data1_1_2)

    # data1_1_2.dropna(inplace=True) # 去掉空值
    # data1_1_2.drop_duplicates(inplace=True)

    a = []

    # 当前科目成绩
    # b = [90, 100, 89, 79, 79, 79, 80, 76, 90]
    b = studentscore

    # 在对应的点
    c = ['●']

    #    print(choosekm)
    #    print("-*-*-*--*-*-*-*-*-*-*-*-")
    #    print(choosekm)

    # for i in ['语文', '数学', '外语']:
    print("科目顺序%s" % choosekm)

    for i in choosekm:
        d = data1_1_2['成绩'][data1_1_2['科目'] == i]
        # print(i)
        a.append([min(d), round(np.mean(d), 1), max(d)])

    #
    plt.rcParams['font.sans-serif'] = ['simhei']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    fig = plt.figure(figsize=(10, 6))  # 建立画布

    titlerequst = ""

    plt.title(titlerequst,
              fontsize='20',
              fontweight='bold',  # 设置字体大小与格式
              color='black',  # 设置字体颜色
              loc='center',  # 设置字体位置
              # verticalalignment='bottom',  # 设置垂直对齐方式
              rotation=0,  # 设置字体旋转角度
              #          bbox=dict(facecolor='white', edgecolor='white', alpha=0.65 )# 标题边框
              )

    # sns.violinplot(x='class', y='hwy', data=datasource, scale='width', inner='quartile', color='green')
    sns.violinplot(x='科目',
                   y='成绩',
                   data=data1_1_2,
                   color='#FA5555',
                   linewidth=1.6,  # 线宽
                   width=0.5,  # 箱之间的间隔比例
                   # palette='hls',  # 设置调色板
                   scale='count',  # 测度小提琴图的宽度： area-面积相同,count-按照样本数量决定宽度,width-宽度一样
                   gridsize=90,  # 设置小提琴图的平滑度，越高越平滑
                   #               order = ['语文', '数学', '外语'], #筛选类别
                   inner='box',  # 设置内部显示类型 --> 'box','quartile','point','stick',None
                   # bw = 0.5,      #控制拟合程度，一般可以不设置
                   cut=0,  # 减去上下分位数
                   #               ax=axes[0] #多个子图内显示箱型图（左边）

                   )

    ###加入显示数字
    for i in range(len(a)):
        for j in range(3):
            plt.text(i - 0.1 + 0.38 * (-j ** 2 + 2 * j), a[i][j] + 5 * (j - 1), a[i][j], fontdict={'size': 13})

    #
    for k in range(len(b)):
        plt.text(k + 0.3, b[k], b[k], fontdict={'size': 13, 'color': '#E10601'})

        for l in range(len(b)):
            plt.text(k - 0.01, b[k], c[0], fontdict={'size': 5, 'color': '#E10601'})

    ###设置显示
    # ax = fig.gca()
    #
    # ax.set_xlabel(" ")
    # ax.spines['top'].set_color('none')  # 设置上边框为透明
    # ax.spines['right'].set_color('none')  # 设置右边框为透明
    # plt.show()

    ###保存为图片
    img_path = r'E:\AutoTest_PY\\'
    # timeslmp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%f')
    # img_path = r'./'
    # imagename = exclname + ".png"
    choosekm=str(choosekm)
    stuId=str(stuId)
    plt.savefig(img_path + stuId +choosekm)
    url=(img_path + stuId +choosekm)+'.png'
    # print(url)
    return url
    # help(sns.violinplot())

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


def getkmlist(datasource, kmlist):
    # 产生唯一列名
    foruseok = pd.DataFrame(pd.read_json(datasource))
    data1_use = foruseok.drop_duplicates(["科目"])
    xklistbypic = data1_use.iloc[0:3, 2:3].values

    usexklist = []
    for i in xklistbypic:
        usexklist.append(get_key(kmlist, i))
    return usexklist



#app.run()
if '__name__' == 'main':
  print('run if')

  app.run(host='0.0.0.0',port='8030',body=800)
else:
  print('run else')
  app.run(host='0.0.0.0',port='8030',body=800)