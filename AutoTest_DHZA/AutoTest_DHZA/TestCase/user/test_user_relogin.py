import  unittest
import requests
import time
import json
import logging
from Common import encryption
from Common import Reids
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
uuid=encryption.Encryption()
key=uuid.get_uuid()
re=Reids.Redis()
cf=Read_config.ReadConfig()



class test_user_relogin(BaseCase):

    def test_usre_relogin_1_getcode(self): #传uuid生成对应的验证码
        data=self.get_case_data("test_usre_relogin_1_getcode")
        data1=key
        check=self.send_request(data,datavariable=data1)
        self.assertIn('200',check)

    def test_usre_relogin_2_login(self): #重置密码用户登录
        time.sleep(3)
        verifyCode=re.get_uuid_key(key)
        data1=key+','+verifyCode
        data=self.get_case_data("test_usre_relogin_2_login")
        check=self.send_request(data,datavariable=data1)
        self.assertIn('登录成功',check)
        request = json.loads(check)
        token = request.get('data').get('token')
        logintoken='Bearer '+token
        cf.set_userdatainfo('logintoken',logintoken)



