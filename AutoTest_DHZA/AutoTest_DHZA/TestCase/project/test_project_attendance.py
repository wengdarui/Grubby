import  time
import datetime
import json
import re
from Common import encryption
from Common import Reids
from Common import DB
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
db=DB.DB_enterprise()
re=Reids.Redis()
logintoken=cf.get_userdatainfo('logintoken')
addemployeeid=cf.get_employeeinfo('addemployeeid')

class test_project_attendance(BaseCase):
    def test_get_dayattendance(self): # 获取日度考勤列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid
        data=self.get_case_data("test_get_dayattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_get_monthattendance(self): # 获取月度考勤列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid
        data=self.get_case_data("test_get_monthattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_get_personattendance(self): # 获取个人考勤列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid+','+addemployeeid
        data=self.get_case_data("test_get_personattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_down_personattendance(self): # 生成个人考勤列表excel
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid+','+addemployeeid
        data=self.get_case_data("test_get_personattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_down_dayattendance(self): # 生成日度考勤列表excel
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid
        data=self.get_case_data("test_down_dayattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_down_monthattendance(self): # 生成月度考勤列表excel
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=projectid+','+groupid
        data=self.get_case_data("test_down_monthattendance")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)