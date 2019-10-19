#!usr/bin/env python
# encoding:utf-8

import  requests
import  ast
import xlrd
import xlwt
import xlutils
import os
import bcrypt
import json
import logging
import re
import xlrd
import random
import time
from xlutils.copy import copy
from Common.DB import *
from Common import Reids
from Common import encryption
from Common import Log
from Common import encryption
from Common import Read_config
from Common.Read_Excel import *
import pdfkit


# uuid=encryption.Encryption()
# key=uuid.get_uuid()
# cf=Read_config.ReadConfig()
# re=Reids.Redis()
# logintoken=cf.get_userdatainfo('logintoken')


# from Common.BaseCase import BaseCase
# class test_user_login(BaseCase):   # 这里直接继承BaseCase
#     def test_usre_login_2_login(self):
#         # """level1:正常登录"""
#         # verifyCode='abcd'
#         data=self.get_case_data("test_usre_login_2_login")
#         # data1=key+','+verifyCode
#         # check=self.send_request(data,datavariable=data1)
#         # print(check,type(check))
#         # print(11)
#
#
# if __name__ == '__main__':
#     a=test_user_login()
#     a.test_usre_login_2_login()


# check='{"code":200,"msg":"success","data":{"projectId":25,"projectCompanyId":39,"joinSuccess":0,"joinFail":0}}'
# request = json.loads(check)
# print(request)
# projectCompanyId=request.get('data').get('projectCompanyId')
# print(projectCompanyId)

# td = datetime.timedelta(hours=+10)
# print(td)
# print(datetime.datetime.utcnow().isoformat())
# print((datetime.datetime.utcnow() + td).isoformat())

uuid=encryption.Encryption()
redis=Reids.Redis()
key=uuid.get_uuid()

code=[
  "com.dh4cloud.versatile.util.ImageCodeGenUtil$ImageCode",
  {
    "code": "RN69",
    "base64": "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAABY0lEQVR42u3YQWrDMBAFUC/aRXqD7nuBXqD3yB1CIOT+tIuCEZIsKzTFGvt9tEikQOBhjUaevqU7EwJYY2CdXj+rI/vZy+V9HktL6eTH5S0dO8fKvB7CyqSWvL6mczoiYbUnU6zMK5us6pRYmdQmZKNgtf+01Nkn1vy5ulTdgI3HanVydKxq2SqxZq8erMwrPFZngU+/trHKYn9orPJBW6ruS1hlzYq6Ddv9wV+wGqdhMKzVAl89Hx/FGqF7eDLWPN9uGhp9Vn8fH7V1KOdX2/cSa7V72La6/wvW71I/VufdcPP2Pdhbh3h3Q69oBBYsWLBgwRJYsGDBggVLYMGCBQsWLIEFCxYsWLAEFixYsGDBEliwYMGCBUtgwYIFCxYsgQULFixYsAQWLFiwYMESWLBgwYIFa8Rc7zdYsI7hBQvWMU/DobxgwYIFK5IXLFhHvkgP4gVrd1i2ISxYAgsWLFjx8gO9LC2JJLtcmAAAAABJRU5ErkJggg=="
  }
]


print(code[1].get("code"),type(code[1]))