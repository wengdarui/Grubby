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
# user_phone=17000000012
subject_list=[4,5,6,7,8,9]
subject_all_list=[1,2,3,4,5,6,7,8,9]
hschool_subject_group_list=[]
user_subject_list=[]
subject_avg=[]
subject_class_avg=[]
subject_ratio=[]
class_list=[]

db=Connect_Mysql.DB()
timeslmp=datetime.datetime.now().strftime('%Y-%m-%d')




##########查询sql
# 查询用户信息
user_info_sql=''' SELECT u.id,i.hschool_id,c.grade_id,i.student_no,c.title,c.id,i.user_name FROM tab_user u LEFT JOIN tab_user_info i ON u.id = i.user_id LEFT JOIN tab_class c ON i.class_id = c.id WHERE u.phone=%s '''
# 最近一次考试考试id
examid_sql='''SELECT id,title,total_num,input_num,start_date from tab_exam WHERE hschool_id=%s AND stat_flag=1 AND term_id in (1,2) AND subject_id=0  ORDER BY end_date DESC LIMIT 1 '''
# 用户所有考试考试id
allexamid_sql='''SELECT id,title,total_num,input_num,start_date from tab_exam WHERE hschool_id=%s AND stat_flag=1 AND term_id in (1,2) AND subject_id=0 '''

#当前用户单科分数等级
score_sql='''SELECT s.title,ss.score,ss.subject_level,ss.score_gap,ss.hexam_score,ss.hexam_score_gap from tab_exam_subject_score2 ss LEFT JOIN tab_subject s ON ss.subject_id=s.id WHERE ss.user_id= %s AND ss.exam_id= %s; '''
#学校开放的选科组合
hschool_subject_group_sql=''' SELECT subject_group_id from tab_r_hschool_subject_group WHERE hschool_id=%s AND grade_id=%s AND class_id IS NULL; '''
#当前用户总分等级(有选科)
allscore_sql = '''SELECT s.title,ss.score,ss.group_level,ss.score_gap from tab_exam_total_score2 ss LEFT JOIN tab_subject_group s ON ss.subject_group_id=s.id LEFT JOIN tab_user_subject_group sg on sg.user_id=ss.user_id
 WHERE ss.user_id= %s AND ss.exam_id= %s AND sg.subject_group_id=ss.subject_group_id; '''
#当前用户总分等级(没有选科取最高分)
allscore_hschool_sql= '''SELECT
	s.title,
	ss.score,
	ss.group_level,
	ss.score_gap
FROM
	tab_exam_total_score2 ss
LEFT JOIN tab_subject_group s ON ss.subject_group_id = s.id
WHERE
	ss.user_id = %s
AND ss.exam_id = %S
AND ss.subject_group_id in (%s)
ORDER BY score DESC LIMIT 1; '''
#最近一次考试年级单科人数
subject_number_sql = ''' SELECT s.title,COUNT(ss.subject_id) from tab_exam_subject_score2 ss LEFT JOIN tab_subject s on ss.subject_id=s.id WHERE ss.exam_id=%s  AND ss.subject_id not in (1,2,3) GROUP BY ss.subject_id ; '''
#最近一次考试班级单科平均分
subject_class_avg_sql = ''' SELECT ROUND(AVG(ss.score),2),s.title from tab_exam_subject_score2 ss LEFT JOIN tab_subject s on ss.subject_id=s.id WHERE ss.exam_id=%s AND ss.subject_id = %s
AND ss.user_id in (SELECT user_id from tab_user_info i LEFT JOIN tab_class c on i.class_id=c.id WHERE c.id=%s); '''
#最近一次考试年级单科平均分
subject_avg_sql = ''' SELECT ROUND(AVG(ss.score),2),s.title from tab_exam_subject_score2 ss LEFT JOIN tab_subject s on ss.subject_id=s.id WHERE ss.exam_id=%s AND ss.subject_id = %s; '''
#当前用户选科
user_subject_sql=''' SELECT s1.title,s2.title,s3.title FROM tab_user_subject us LEFT JOIN tab_subject s1 ON us.subject1=s1.id LEFT JOIN tab_subject s2 ON us.subject2=s2.id LEFT JOIN tab_subject s3 ON us.subject3=s3.id WHERE us.user_id = %s; '''
#当前用户多志愿
user_subject_group_sql = ''' SELECT s.title,s1.title,s2.title from tab_user_subject_group sg LEFT JOIN tab_subject_group s ON sg.subject_group_id=s.id
LEFT JOIN tab_subject_group s1 ON sg.subject_group_id2=s1.id LEFT JOIN tab_subject_group s2 ON sg.subject_group_id3=s2.id WHERE sg.user_id=%s; '''
#最近一次考试所有组合的分数等级
user_allsubject_score_sql= ''' SELECT g.title,s.score,s.group_level FROM tab_exam_total_score2 s LEFT JOIN tab_subject_group g ON s.subject_group_id=g.id WHERE s.user_id=%s AND s.exam_id=%s ORDER BY score DESC; '''
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
	r.user_id = 84253;'''

#最近一次考试对应用户多次选科组合的分数
user_previouslysubject_score_sql=''' SELECT g.title,s.score,s.group_level
FROM
	tab_exam_total_score2 s
LEFT JOIN tab_subject_group g ON s.subject_group_id = g.id
WHERE
	s.user_id =%s
AND s.exam_id =%s
AND s.subject_group_id=%s '''

#定义运行当前脚本;解决中文乱码#定义路径和方法
server = flask.Flask(__name__)
server.config['JSON_AS_ASCII'] = False
@server.route('/h5test',methods=['get','post'])

##########执行sql
def run_sql():
    user_phone=flask.request.values.get('user_phone')
    try:
        user_info=db.connect1(user_info_sql,user_phone)
        for i in user_info:
            user_id=i[0]
            hschool_id=i[1]
            grade_id=i[2]
            student_no=i[3]
            class_name=i[4]
            class_id=i[5]
            user_name=i[6]

        examid=db.connect1(examid_sql,hschool_id)
        for i in examid:
            examid=i[0]
            exam_title=i[1]
            exam_total_num=i[2]
            exam_input_num=i[3]
            exam_date=i[4]
        allexamid=db.connect1(allexamid_sql,hschool_id)


        score=db.connect2(score_sql,user_id,examid)
        allscore=db.connect2(allscore_sql,user_id,examid)
        time.sleep(2)
        subject_class_avg.clear()
        subject_avg.clear()
        for i in subject_all_list:
            fen=db.connect3(subject_class_avg_sql,examid,i,class_id)
            subject_class_avg.append(fen)
        for i in subject_all_list:
            fen=db.connect2(subject_avg_sql,examid,i)
            subject_avg.append(fen)
        user_subject=db.connect1(user_subject_sql,user_id)

        user_subject_group=db.connect1(user_subject_group_sql,user_id)

        user_allsubject_score=db.connect2(user_allsubject_score_sql,user_id,examid)
    except Exception as e:
        print('执行sql异常信息:%s'%e)

    # 三门主科成绩分析
    # Main_subjects={'语文':0,'数学':0,'外语':0}
    # try:
    #     for i in score:
    #         if i[0]=='语文':
    #             Main_subjects.update({'语文':i[1]})
    #         elif i[0]=='数学':
    #             Main_subjects.update({'数学':i[1]})
    #         elif i[0]=='外语':
    #                 Main_subjects.update({'外语':i[1]})
    #         else:
    #             continue
    #     if max(Main_subjects.values())-min(Main_subjects.values())>40:
    #         Main_subjects_result=('%s表现更佳，位于年级前X；%s波动较大，需投入更多精力。'%(max(Main_subjects.keys()),min(Main_subjects.keys())))
    #     elif min(Main_subjects.values())>99:
    #         Main_subjects_result=('你的主科旗鼓相当，为选考科目腾出极大的精力，KEEP才是关键！')
    #     elif max(Main_subjects.values())<100:
    #             Main_subjects_result=('你在危险地带徘徊，主科是高考分数大头，当务之急先拿下基础分，再做单科提升！')
    #     else: Main_subjects_result=('都不符合')
    #
    # except Exception as e:
    #     print('三门主科成绩分析异常信息:%s'%e)

    #本次考试成绩分析
    try:
        user_subject_list.clear()
        for i in user_subject:
            if i[0] not in ('物理','历史'):
                user_subject_list.append(i[0])
            elif i[1] not in ('物理','历史'):
                user_subject_list.append(i[1])
                if i[2] not in ('物理','历史'):
                    user_subject_list.append(i[2])
        if len(score)>6:
            NotMain_subjects_result=('本次考试成绩与选科对比%s\n%s'%(user_subject_list,score))
        else:
            NotMain_subjects_result=('综合年级位次、平均分，A学科实力低于B，不偏科才是正确姿势。判定依据：年级位次比较、两门学科与平均分相比，看差额。')
    except Exception as e:
        print('三门主科成绩分析异常信息:%s'%e)

    res = {'user_info':{'用户id':user_id,'用户姓名':user_name, '学校id':hschool_id, '年级id':grade_id, '学号':student_no, '班级名字':class_name, '班级id': class_id},
           'exam_info':{'考试id':examid, '考试名称':exam_title, '应考人数':exam_total_num,'参加考试人数':exam_input_num,'考试时间':exam_date},
           'allexam_info':{'全部考试':allexamid},
           'exam_user_info':{'本次考试成绩的总分':allscore,'本次考试单科成绩':score,'本次考试所有组合的分数等级':user_allsubject_score},
            'user_subject_group':{'当前用户多志愿':user_subject_group},
           'user_allsubject_score':{'本次考试所有组合的分数等级':user_allsubject_score},
           'exam_class_info':{'本次考试班级单科平均分':subject_class_avg},
           'exam_grade_info':{'本次考试年级单科平均分':subject_avg},
           # 'Main_subjects_result':{'三门主科分析':Main_subjects_result},
           'NotMain_subjects_result':{'（生物，化学，地理，政治）分析':NotMain_subjects_result}}
    return jsonify(res)

server.run(port=7777,debug=True,host='0.0.0.0')



if __name__ == '__main__':
    run_sql()


