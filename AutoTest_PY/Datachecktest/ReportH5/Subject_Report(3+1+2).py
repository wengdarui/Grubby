import os
import time
import datetime
import json
import demjson
import flask
from flask import jsonify
from Common import Connect_Mysql


###参数变量
# user_phone=11100000011
# user_phone=19900000010
subject_list=[4,5,6,7,8,9]
subject_all_list=[1,2,3,4,5,6,7,8,9]
hschool_subject_group_list=[]
user_subject_list=[]
subject_avg=[]
subject_class_avg=[]
subject_ratio=[]
class_list=[]
user_previouslysubject_list=[]



connect=Connect_Mysql.Connect
timeslmp=datetime.datetime.now().strftime('%Y-%m-%d')

##########查询sql
# 查询用户信息
user_info_sql=''' SELECT u.id,i.hschool_id,c.grade_id,i.student_no,c.title,c.id,i.user_name FROM tab_user u LEFT JOIN tab_user_info i ON u.id = i.user_id LEFT JOIN tab_class c ON i.class_id = c.id WHERE u.phone=%s '''
# 最近一次考试考试id
examid_sql='''SELECT id,title,total_num,input_num from tab_exam WHERE hschool_id=%s AND stat_flag=1 AND term_id in (1,2) AND subject_id=0  ORDER BY end_date DESC LIMIT 1 '''
#当前用户单科分数等级
score_sql='''SELECT s.title,ss.score,ss.subject_level,ss.score_gap from tab_exam_subject_score2 ss LEFT JOIN tab_subject s ON ss.subject_id=s.id WHERE ss.user_id= %s AND ss.exam_id= %s; '''
#当前用户总分等级
allacore_sql = '''SELECT s.title,ss.score,ss.group_level,ss.score_gap from tab_exam_total_score2 ss LEFT JOIN tab_subject_group s ON ss.subject_group_id=s.id LEFT JOIN tab_user_subject_group sg on sg.user_id=ss.user_id
 WHERE ss.user_id= %s AND ss.exam_id= %s AND sg.subject_group_id=ss.subject_group_id; '''
#最近一次考试年级单科人数
subject_number_sql = ''' SELECT s.title,COUNT(ss.subject_id) from tab_exam_subject_score2 ss LEFT JOIN tab_subject s on ss.subject_id=s.id WHERE ss.exam_id=%s  AND ss.subject_id not in (1,2,3) GROUP BY ss.subject_id ; '''
#最近一次考试年级单科平均分
subject_avg_sql = ''' SELECT ROUND(AVG(ss.score),2),s.title from tab_exam_subject_score2 ss LEFT JOIN tab_subject s on ss.subject_id=s.id WHERE ss.exam_id=%s AND ss.subject_id = %s; '''
#当前用户多志愿
user_subject_group_sql = ''' SELECT s.title,s1.title,s2.title from tab_user_subject_group sg LEFT JOIN tab_subject_group s ON sg.subject_group_id=s.id
LEFT JOIN tab_subject_group s1 ON sg.subject_group_id2=s1.id LEFT JOIN tab_subject_group s2 ON sg.subject_group_id3=s2.id WHERE sg.user_id=%s; '''
#最近一次考试所有组合的分数等级
user_allsubject_score_sql= ''' SELECT g.title,s.score,s.group_level FROM tab_exam_total_score2 s LEFT JOIN tab_subject_group g ON s.subject_group_id=g.id WHERE s.user_id=%s AND s.exam_id=%s ORDER BY score DESC; '''
#本次选科不同组合的总人数
hschool_allsubject_allnumber_sql=''' SELECT
COUNT(*)
FROM
tab_grade g
LEFT JOIN tab_class c ON g.id=c.grade_id
LEFT JOIN tab_user_info i ON c.id = i.class_id
LEFT JOIN tab_user u ON i.user_id=u.id
LEFT JOIN tab_user_subject_group sg on i.user_id=sg.user_id
LEFT JOIN tab_subject_group tg on sg.subject_group_id=tg.id
WHERE
g.id = %s
AND u.role=1
AND sg.subject_group_id IS not NULL '''
#本次选科不同组合的人数分布
hschool_allsubject_number_sql= '''SELECT
tg.title,COUNT(sg.subject_group_id) number
FROM
tab_grade g
LEFT JOIN tab_class c ON g.id=c.grade_id
LEFT JOIN tab_user_info i ON c.id = i.class_id
LEFT JOIN tab_user u ON i.user_id=u.id
LEFT JOIN tab_user_subject_group sg on i.user_id=sg.user_id
LEFT JOIN tab_subject_group tg on sg.subject_group_id=tg.id
WHERE
g.id = %s
AND u.role=1
AND sg.subject_group_id IS not NULL
GROUP BY sg.subject_group_id
ORDER BY COUNT(sg.subject_group_id) DESC;
'''
#当前用户的目标
user_aim_sql=''' SELECT
	h.title,
	m.title
FROM
	tab_aim a
LEFT JOIN tab_school h ON a.school_id = h.id
LEFT JOIN tab_school_major m ON a.school_major_id = m.id
WHERE
	a.user_id = %s
AND a.`status` = 1; '''


#多次成绩
allexamid_list=[]
user_allexam_subjectscore_list=[]
user_previouslysubject_score_list=[]


# 用户所有考试id
allexamid_sql='''SELECT id,title from tab_exam WHERE hschool_id=%s AND stat_flag=1 AND term_id in (1,2) AND subject_id=0  ORDER BY end_date DESC; '''

#多次成绩最高分组合
user_allexam_subjectscore_sql=''' SELECT
e.title,g.title,s.score,s.group_level
FROM
	tab_exam_total_score2 s
LEFT JOIN tab_subject_group g ON s.subject_group_id = g.id
LEFT JOIN tab_exam e on e.id=s.exam_id
WHERE
	s.user_id =%s
AND s.exam_id =%s
ORDER BY
	score DESC
LIMIT 1; '''

#用户历次选科活动结果

user_previouslysubject_sql=''' SELECT s.title,g.title,r.subject_group_id
FROM
	tab_user_subject_group_sel_record r
LEFT JOIN tab_hschool_sel_subject s ON r.hschool_sel_subject_id = s.id
LEFT JOIN tab_subject_group g on r.subject_group_id=g.id
WHERE
	r.user_id = %s;'''

#最近一次考试对应用户多次选科组合的分数
user_previouslysubject_score_sql=''' SELECT g.title,s.score,s.group_level
FROM
	tab_exam_total_score2 s
LEFT JOIN tab_subject_group g ON s.subject_group_id = g.id
WHERE
	s.user_id =%s
AND s.exam_id =%s
AND s.subject_group_id=%s '''

#定义运行当前脚本;结果中文乱码#定义路径和方法
server = flask.Flask(__name__)
server.config['JSON_AS_ASCII'] = False
@server.route('/h5test',methods=['get','post'])


##########执行sql
def run_sql():
    user_phone=flask.request.values.get('user_phone')
    try:
        user_info=connect.connect1(user_info_sql,user_phone)
        for i in user_info:
            user_id=i[0]
            hschool_id=i[1]
            grade_id=i[2]
            student_no=i[3]
            class_name=i[4]
            class_id=i[5]
            user_name=i[6]

    except Exception as e:
        print('异常信息:%s'%e)

    try:
        examid=connect.connect1(examid_sql,hschool_id)
        for i in examid:
            examid=i[0]
            exam_title=i[1]
            exam_total_num=i[2]
            exam_input_num=i[3]
        score=connect.connect2(score_sql,user_id,examid)
        allscore=connect.connect2(allacore_sql,user_id,examid)
        subject_number=connect.connect1(subject_number_sql,examid)

        for i in subject_list:
            fen=connect.connect2(subject_avg_sql,examid,i)
            subject_avg.append(fen)

        user_subject_group=connect.connect1(user_subject_group_sql,user_id)

        user_allsubject_score=connect.connect2(user_allsubject_score_sql,user_id,examid)

        hschool_allsubject_number=connect.connect1(hschool_allsubject_number_sql,grade_id)

        hschool_allsubject_allnumber=connect.connect1(hschool_allsubject_allnumber_sql,grade_id)

        for i in hschool_allsubject_allnumber:
            hschool_allsubject_allnumber=i[0]

        for i in range(len(hschool_allsubject_number)):
            number= hschool_allsubject_number[i][1]
            subjectratio= round(number/hschool_allsubject_allnumber,2)
            subject_ratio.append( hschool_allsubject_number[i][0])
            subject_ratio.append(subjectratio)

    except Exception as e:
        print('异常信息:%s'%e)

    try:
        allexamid=connect.connect1(allexamid_sql,hschool_id)
        for i in range(len(allexamid)):
            allexamid_list.append(allexamid[i][0])

        for i in range(len(allexamid_list)):
            user_allexam_subjectscore_list.append(connect.connect2(user_allexam_subjectscore_sql,user_id,allexamid_list[i]))


        user_previouslysubject=connect.connect1(user_previouslysubject_sql,user_id)

        for i in range(len(user_previouslysubject)):
            user_previouslysubject_score_list.append(connect.connect3(user_previouslysubject_score_sql,user_id,allexamid_list[i],user_previouslysubject[i][2]))

        user_aim=connect.connect1(user_aim_sql,user_id)
        for i in user_aim:
            user_aim=user_aim[0]
    except Exception as e:
        print('异常信息:%s'%e)

    res = {'user_info':{'用户id':user_id,'用户姓名':user_name, '学校id':hschool_id, '年级id':grade_id, '学号':student_no, '班级名字':class_name, '班级id': class_id},
           'exam_info':{'考试id':examid, '考试名称':exam_title, '应考人数':exam_total_num,'参加考试人数':exam_input_num,'最近一次考试单科人数':subject_number,'最近一次考试单科人数':subject_number,'最近一次考试年级单科平均分':subject_avg},
           'exam_user_info':{'本次考试成绩的总分':allscore,'本次考试单科成绩':score,'本次考试所有组合的分数等级':user_allsubject_score},
            'hschool_allsubject_info':{'本次选科不同组合的人数分布':hschool_allsubject_number,'本次选科组合人数占比':subject_ratio},
           'allexam_user_info':{'当前用户的所有考试':allexamid,'当前用户历次选科组合':user_previouslysubject,'当前用户历次选科组合对应最后一次考试的成绩':user_previouslysubject_score_list},
           'user_aim_info':{'当前用户的目标':user_aim}
           }
    return jsonify(res)


server.run(port=7777,debug=True,host='0.0.0.0')


# print("用户id：%s 用户姓名：%s 学校id：%s 年级id：%s 学号：%s 班级名字：%s 班级id %s " %(user_id,user_name,hschool_id,grade_id,student_no,class_name,class_id))
# print('该用户最近一次考试成绩的总分%s=====本次考试单科成绩%s'%(allscore,score))
# print('最近一次考试单科人数{}'.format(subject_number))
# print('最近一次考试年级单科平均分%s'%subject_avg)
# print('当前用户多志愿%s'%user_subject_group)
# print('最近一次考试所有组合的分数等级{}'.format(user_allsubject_score))
# print('本次选科不同组合的人数分布{}'.format(hschool_allsubject_number))
# print('本次选科组合人数占比%s'%subject_ratio)
# print('当前用户的目标{}'.format(user_aim))
# print('当前用户的所有考试{}'.format(allexamid))
# print('当前用户历次选科组合{}'.format(user_previouslysubject))
# print('当前用户历次选科组合对应最后一次考试的成绩{}'.format(user_previouslysubject_score_list))

if __name__ == '__main__':
    run_sql()
