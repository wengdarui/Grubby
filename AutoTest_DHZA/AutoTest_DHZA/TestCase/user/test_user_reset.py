import  unittest
import requests
import time
import json
import logging
import random
from Common import Reids
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
re=Reids.Redis()
cf=Read_config.ReadConfig()
rephone=cf.get_userdatainfo('not_exist_phone')



class test_user_reset(BaseCase):

    def test_user_reset_1_code(self): #获取验证码
        data=self.get_case_data("test_user_reset_1_code")
        check=self.send_request(data)
        self.assertIn('success',check)

    def test_usre_reset_2_pwd(self): #重置密码
        time.sleep(3)
        verifyCode=re.get_reset_code(rephone)
        data=self.get_case_data("test_usre_reset_2_pwd")
        check=self.send_request(data,datavariable=verifyCode)
        self.assertIn('操作成功',check)