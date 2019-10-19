import  time
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


class test_project_worksurface(BaseCase):
    def test_add_worksurface(self): #添加资源模型文件
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        resourceid=cf.get_project('resourceid')
        data_value=resourceid+','+projectid
        data=self.get_case_data("test_add_worksurface")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)
        request = json.loads(check)
        worksurfaceid=request.get('data')
        cf.set_project('worksurfaceid',str(worksurfaceid))

    def test_get_worksurfacelist(self): #获取资源模型文件列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_worksurfacelist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_getpage_worksurfacelist(self): #获取资源模型文件列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_getpage_worksurfacelist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_get_worksurfaceinfo(self): #获取资源模型文件列表
        time.sleep(2)
        cf=Read_config.ReadConfig()
        worksurfaceid=cf.get_project('worksurfaceid')
        data=self.get_case_data("test_get_worksurfaceinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=worksurfaceid)
        self.assertIn('success',check)


