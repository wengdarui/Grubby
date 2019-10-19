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
addemployeeid=cf.get_employeeinfo('addemployeeid')


class test_project_manage(BaseCase):
    def test_enter_buildenterprise(self): #进入施工方企业
        cf=Read_config.ReadConfig()
        buildenterpriseid=cf.get_enterpriseinfo('buildenterpriseid')
        data=self.get_case_data("test_enter_enterprise")
        check=self.send_request(data,headersvariable=logintoken,datavariable=buildenterpriseid)
        self.assertIn('success',check)

    def test_buildenterprise_addproject(self): #施工方企业加入项目
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        inviteid=cf.get_project('inviteid')
        data_value=addemployeeid+','+inviteid+','+projectid
        data=self.get_case_data("test_buildenterprise_addproject")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)
        request = json.loads(check)
        projectCompanyId=request.get('data').get('projectCompanyId')
        cf.set_project('buildpcid',str(projectCompanyId))

    def test_buildenterprise_chcekproject(self): #检查施工方企业是否已加入项目
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_buildenterprise_chcekproject")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_enter_checkenterprise(self): #进入监理方企业
        cf=Read_config.ReadConfig()
        checkenterpriseid=cf.get_enterpriseinfo('checkenterpriseid')
        data=self.get_case_data("test_enter_checkenterprise")
        check=self.send_request(data,headersvariable=logintoken,datavariable=checkenterpriseid)
        self.assertIn('success',check)

    def test_checkenterprise_addproject(self): #监理方企业加入项目
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        cf=Read_config.ReadConfig()
        inviteid=cf.get_project('inviteid')
        data_value=addemployeeid+','+inviteid+','+projectid
        data=self.get_case_data("test_checkenterprise_addproject")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)
        request = json.loads(check)
        projectCompanyId=request.get('data').get('projectCompanyId')
        cf.set_project('checkpcid',str(projectCompanyId))

    def test_checkenterprise_chcekproject(self): #检查监理方企业是否已加入项目
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_checkenterprise_chcekproject")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_enter_enterprise(self): #进入业主方企业
        cf=Read_config.ReadConfig()
        enterpriseid=cf.get_enterpriseinfo('enterpriseid')
        data=self.get_case_data("test_enter_enterprise")
        check=self.send_request(data,headersvariable=logintoken,datavariable=enterpriseid)
        self.assertIn('success',check)

    def test_getpmlist_project(self): #业主方获取项目企业列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_getpmlist_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

    def test_setbuild_project(self): #设置施工方企业为项目施工方
        time.sleep(2)
        cf=Read_config.ReadConfig()
        buildpcid=cf.get_project('buildpcid')
        data=self.get_case_data("test_setbuild_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=buildpcid)
        self.assertIn('success',check)

    def test_getbuild_projectinfo(self): #检查施工方企业在项目中的信息
        cf=Read_config.ReadConfig()
        buildpcid=cf.get_project('buildpcid')
        data=self.get_case_data("test_getbuild_projectinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=buildpcid)
        self.assertIn('success',check)


    def test_setcheck_project(self): #设置监理方企业为项目施工方（并且监管施工方企业）
        cf=Read_config.ReadConfig()
        buildpcid=cf.get_project('buildpcid')
        checkpcid=cf.get_project('checkpcid')
        data_value=checkpcid+','+buildpcid
        data=self.get_case_data("test_setcheck_project")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)

    def test_getcheck_projectinfo(self): #检查监理方企业在项目中的信息
        cf=Read_config.ReadConfig()
        checkpcid=cf.get_project('checkpcid')
        data=self.get_case_data("test_getbuild_projectinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=checkpcid)
        self.assertIn('success',check)

    def test_getbuildlist_project(self): #检查项目中的所有施工方信息
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_getbuild_projectinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('success',check)

