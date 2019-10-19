import  time
import json
import re
from Common import DB
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
db=DB.DB_enterprise()
logintoken=cf.get_userdatainfo('logintoken')

class test_add_project(BaseCase):
    def test_add_newproject(self): #创建新项目
        cf=Read_config.ReadConfig()
        adddepartmentid=cf.get_departmentinfo('adddepartmentid')
        data=self.get_case_data("test_add_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=adddepartmentid)
        self.assertIn('success',check)
        request = json.loads(check)
        pjid = str(request.get('data').get('id'))
        cf.set_project('projectid',pjid)

    def test_get_projectlist(self):
        time.sleep(2)
        data=self.get_case_data("test_get_projectlist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_setaddress_project(self): #设置项目地址
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_setaddress_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_setname_project(self): #设置项目名称
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_setname_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_get_projectinfo(self): #获取项目信息
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_projectinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_inviteurl_project(self): #生成项目邀请链接
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_inviteurl_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)
        request = json.loads(check)
        ivurl = str(request.get('data'))
        reiv="id=(.*)"
        getid = re.findall(reiv,ivurl)
        cf.set_project('inviteid',getid[0])

    def test_inviteinfo_project(self): #邀请链接信息
        time.sleep(2)
        cf=Read_config.ReadConfig()
        inviteid=cf.get_project('inviteid')
        data=self.get_case_data("test_inviteinfo_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=inviteid)
        self.assertIn('success',check)


