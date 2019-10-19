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
worksurfaceid=cf.get_project('worksurfaceid')
addemployeeid=cf.get_employeeinfo('addemployeeid')
addemployeeid2=cf.get_employeeinfo('addemployeeid2')



class test_project_group(BaseCase):
    def test_add_group(self): # 添加考勤组
        cf=Read_config.ReadConfig()
        rulesid=cf.get_project('rulesid')
        projectid=cf.get_project('projectid')
        data_value=worksurfaceid+','+addemployeeid+','+rulesid+','+addemployeeid+','+projectid+','+addemployeeid
        data=self.get_case_data("test_add_group")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)
        request = json.loads(check)
        groupid=request.get('data')
        cf.set_project('groupid',str(groupid))

    def test_get_grouplist(self): # 获取考勤组列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_grouplist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('200',check)

    def test_get_groupworklist(self): # 获取考勤组设置作业面列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_groupworklist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('200',check)

    def test_update_groupinfo(self): # 更新考勤组基本信息
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        rulesid=cf.get_project('rulesid')
        data_value=rulesid+','+addemployeeid+','+addemployeeid2+','+addemployeeid2+','+groupid+','+projectid+','+addemployeeid2
        data=self.get_case_data("test_update_groupinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_update_groupwork(self): # 更新考勤组工作面信息
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        rulesid=cf.get_project('rulesid')
        data_value=rulesid+','+groupid+','+projectid
        data=self.get_case_data("test_update_groupwork")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

    def test_get_groupinfo(self): # 获取考勤组信息
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        groupid=cf.get_project('groupid')
        data_value=groupid+','+projectid
        data=self.get_case_data("test_get_groupinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)

