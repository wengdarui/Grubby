import  unittest
import requests
import time
import json
import logging
import ast
from Common import encryption
from Common import Reids
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
logintoken=cf.get_userdatainfo('logintoken')


class test_add_enterprise(BaseCase):

    def test_add_mainenterprise(self): #添加主体企业
        data=self.get_case_data("test_add_mainenterprise")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)
        request = json.loads(check)
        enid = str(request.get('data').get('id'))
        cf.set_enterpriseinfo('enterpriseid',enid)

    def test_add_buildenterprise(self): #添加施工方企业
        data=self.get_case_data("test_add_buildenterprise")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)
        request = json.loads(check)
        enid = str(request.get('data').get('id'))
        cf.set_enterpriseinfo('buildenterpriseid',enid)

    def test_add_checkenterprise(self): #添加监理方企业
        data=self.get_case_data("test_add_checkenterprise")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)
        request = json.loads(check)
        enid = str(request.get('data').get('id'))
        cf.set_enterpriseinfo('checkenterpriseid',enid)

    def test_add_repeat_enterprise(self): #添加重复的企业
        data=self.get_case_data("test_add_repeat_enterprise")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('已存在',check)

    def test_check_enterpriselist(self): #查询我的企业列表
        data=self.get_case_data("test_check_enterpriselist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enter_enterprise(self): #进入添加的主体企业
        cf=Read_config.ReadConfig()
        enterpriseid=cf.get_enterpriseinfo('enterpriseid')
        data=self.get_case_data("test_enter_enterprise")
        check=self.send_request(data,headersvariable=logintoken,datavariable=enterpriseid)
        self.assertIn('success',check)

