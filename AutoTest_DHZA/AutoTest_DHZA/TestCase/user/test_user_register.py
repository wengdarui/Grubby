import  unittest
import requests
import time
import json
import random
import logging
from Common import Reids
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
re=Reids.Redis()
cf=Read_config.ReadConfig()
notphone=cf.get_userdatainfo('not_exist_phone')



class test_user_register(BaseCase):

    def test_user_register_1_code(self): #获取验证码
        data=self.get_case_data("test_user_register_1_code")
        check=self.send_request(data)
        self.assertIn('success',check)

    def test_user_register_2_check(self): #判断手机号是否注册（true/false）
        data=self.get_case_data("test_user_register_2_check")
        check=self.send_request(data)
        self.assertIn('false',check)

    def test_user_register_3_checkcode(self): # 验证手机号和验证码
        time.sleep(2)
        code=re.get_register_code(notphone)
        data=self.get_case_data("test_user_register_3_checkcode")
        check=self.send_request(data,datavariable=code)
        self.assertIn('true',check)

    def test_user_register_4_register(self): # 注册用户
        time.sleep(2)
        code=re.get_register_code(notphone)
        data=self.get_case_data("test_user_register_4_register")
        check=self.send_request(data,datavariable=code)
        self.assertIn('操作成功',check)





