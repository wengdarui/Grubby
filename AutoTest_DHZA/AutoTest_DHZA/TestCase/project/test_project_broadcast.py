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
projectid=cf.get_project('projectid')
groupid=cf.get_project('groupid')

# class test_project_broadcast(BaseCase):
#     def test_add_broadcast(self): # 添加考勤组广播
#         data=self.get_case_data("test_add_broadcast")
#         check=self.send_request(data,headersvariable=logintoken,datavariable=groupid)
#         self.assertIn('200',check)
