import  unittest
import json
import time
from Common import DB
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
db=DB.DB_enterprise()
logintoken=cf.get_userdatainfo('logintoken')

class test_add_department(BaseCase):

    def test_check_departmentlist(self): #查询部门树
        data=self.get_case_data("test_check_departmentlist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)
        request = json.loads(check)
        deid = str(request.get('data')[0].get('id'))
        cf.set_departmentinfo('departmentid',deid)

    def test_check_employeelist(self): #查询部门员工树
        data=self.get_case_data("test_check_employeelist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)


    def test_updatename_department(self): #修改根部门名称
        time.sleep(2)
        cf=Read_config.ReadConfig()
        departmentid=cf.get_departmentinfo('departmentid')
        data=self.get_case_data("test_updatename_department")
        check=self.send_request(data,headersvariable=logintoken,datavariable=departmentid)
        self.assertIn('操作成功',check)

    def test_add_newdepartment(self): #添加部门
        cf=Read_config.ReadConfig()
        departmentid=cf.get_departmentinfo('departmentid')
        data=self.get_case_data("test_add_newdepartment")
        check=self.send_request(data,headersvariable=logintoken,datavariable=departmentid)
        self.assertIn('success',check)
        request = json.loads(check)
        deid = str(request.get('data').get('id'))
        cf.set_departmentinfo('adddepartmentid',deid)


    def test_search_department(self): #搜素添加的部门
        data=self.get_case_data("test_search_department")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('测试添加部门',check)
