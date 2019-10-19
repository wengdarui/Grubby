from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
logintoken=cf.get_userdatainfo('logintoken')


class test_enterprise_info(BaseCase):  #企业信息、认证、加入企业配置
    def test_enterprise_info(self): #查询企业信息（在进入具体企业后调用）
        data=self.get_case_data("test_enterprise_info")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('200',check)

    def test_enterprise_address(self): #添加或修改企业地址
        data=self.get_case_data("test_enterprise_address")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_logo(self): #添加或修改企业logo
        data=self.get_case_data("test_enterprise_logo")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_phone(self): #添加或修改企业电话
        data=self.get_case_data("test_enterprise_phone")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_web(self): #添加或修改企业官网
        data=self.get_case_data("test_enterprise_web")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_addauthentication(self): #添加或修改企业认证信息
        data=self.get_case_data("test_enterprise_addauthentication")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_authenticationinfo(self): #添加或修改企业认证信息
        data=self.get_case_data("test_enterprise_authenticationinfo")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

    def test_enterprise_updeapplication(self): #修改企业申请加入配置（status：是否需要审核，1需要，默认需要）
        cf=Read_config.ReadConfig()
        departmentid=cf.get_departmentinfo('departmentid')
        data=self.get_case_data("test_enterprise_updeapplication")
        check=self.send_request(data,headersvariable=logintoken,datavariable=departmentid)
        self.assertIn('success',check)

    def test_enterprise_applicationinfo(self): #企业申请加入配置
        data=self.get_case_data("test_enterprise_applicationinfo")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('success',check)

