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


class test_add_employee(BaseCase):

    def test_add_newemployee1(self): #添加员工1
        cf=Read_config.ReadConfig()
        departmentid=cf.get_departmentinfo('adddepartmentid')
        data=self.get_case_data("test_add_newemployee1")
        check=self.send_request(data,headersvariable=logintoken,datavariable=departmentid)
        self.assertIn('success',check)
        request = json.loads(check)
        userid = str(request.get('data'))
        cf.set_employeeinfo('addemployeeid',userid)

    def test_add_newemployee2(self): #添加员工2
        cf=Read_config.ReadConfig()
        departmentid=cf.get_departmentinfo('adddepartmentid')
        data=self.get_case_data("test_add_newemployee2")
        check=self.send_request(data,headersvariable=logintoken,datavariable=departmentid)
        self.assertIn('success',check)
        request = json.loads(check)
        userid = str(request.get('data'))
        cf.set_employeeinfo('addemployeeid2',userid)

    # def test_search_employee(self): #搜素添加的员工
    #     data=self.get_case_data("test_search_employee")
    #     check=self.send_request(data,headersvariable=logintoken)
    #     self.assertIn('测试添加员工',check)

    def test_employee_info(self): #查询员工详情
        time.sleep(2)
        cf=Read_config.ReadConfig()
        userid=cf.get_employeeinfo('addemployeeid')
        data=self.get_case_data("test_employee_info")
        check=self.send_request(data,headersvariable=logintoken,datavariable=userid)
        self.assertIn('测试添加员工',check)

    def test_employee_move(self): #员工移入其他部门
        cf=Read_config.ReadConfig()
        userid=cf.get_employeeinfo('addemployeeid')
        departmentid=cf.get_departmentinfo('departmentid')
        adddepartmentid=cf.get_departmentinfo('adddepartmentid')
        data_value=adddepartmentid+','+userid+','+departmentid
        data=self.get_case_data("test_employee_move")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)


