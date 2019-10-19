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


class test_project_rules(BaseCase):
    def test_add_rules(self): # 添加考勤规则
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_add_rules")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('200',check)
        request = json.loads(check)
        rulesid=request.get('data')
        cf.set_project('rulesid',str(rulesid))

    def test_get_ruleslist(self): # 获取考勤规则列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_ruleslist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('中和施工三队',check)

    def test_update_rules(self): # 修改考勤规则
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        rulesid=cf.get_project('rulesid')
        data_value=rulesid+','+projectid
        data=self.get_case_data("test_update_rules")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)

    def test_get_rulesinfo(self): # 获取考勤规则详情
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        rulesid=cf.get_project('rulesid')
        data_value=rulesid+','+projectid
        data=self.get_case_data("test_get_rulesinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)


