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
addemployeeid2=cf.get_employeeinfo('addemployeeid2')
addemployeeid=cf.get_employeeinfo('addemployeeid')
daytime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
utctime=datetime.datetime.utcnow().isoformat()

class test_project_team(BaseCase):
    def test_add_teamemployee(self): #添加项目人员
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data_value=addemployeeid2+','+projectid
        data=self.get_case_data("test_add_teamemployee")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)

    def test_get_teamemployeelist(self): #获取项目人员列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_teamemployeelist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('测试添加员工2',check)

    def test_dele_teamemployee(self): #删除项目人员
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data_value=addemployeeid2+','+projectid
        data=self.get_case_data("test_dele_teamemployee")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)

