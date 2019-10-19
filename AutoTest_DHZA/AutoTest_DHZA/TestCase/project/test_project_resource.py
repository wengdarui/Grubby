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



class test_project_resource(BaseCase):
    def test_add_resource(self): #添加资源模型文件
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_add_resource")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)
        request = json.loads(check)
        resourceid=request.get('data')
        cf.set_project('resourceid',str(resourceid))

    def test_get_resourcelist(self): #获取资源模型文件列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_resourcelist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_set_resource(self): #资源模型文件申请转换
        time.sleep(2)
        cf=Read_config.ReadConfig()
        resourceid=cf.get_project('resourceid')
        data=self.get_case_data("test_set_resource")
        check=self.send_request(data,headersvariable=logintoken,datavariable=resourceid)
        # 手动更新资源状态为转换成功
        db.updata_data('UPDATE `model_resource` set `status`=2 WHERE id=%s;',resourceid)
        self.assertIn('success',check)

    def test_getpass_resourcelist(self): #获取资源模型文件成功列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_getpass_resourcelist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

