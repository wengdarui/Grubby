import unittest
import requests
import json
import os
import sys
sys.path.append("../..")  # 统一将包的搜索路径提升到项目根目录下

from Common.Read_Excel import *
from Common.case_log import *

data_file='D:/Test/AutoTest_DHZA/AutoTest_DHZA/TestCase/test_user_data.xlsx'




class BaseCase(unittest.TestCase):  # 继承unittest.TestCase
    @classmethod
    def setUpClass(cls):
        if cls.__name__ != 'BaseCase':
            cls.data_list = excel_to_list(data_file, cls.__name__)
    # def __init__(self):
    #     super(BaseCase,self).__init__()
        # if self.__name__ !='BaseCase':
        # self.data_list = excel_to_list(data_file,self.__name__)
    def get_case_data(self, case_name):
        return get_test_data(self.data_list, case_name)

    def send_request(self, case_data,headersvariable=None,datavariable=None):
        variable='%'
        case_name=case_data.get('case_name')
        url = case_data.get('url')
        header = case_data.get('headers')
        data = case_data.get('data')
        method = case_data.get('method')
        # expect_res = case_data.get('expect_res')
        # data_type = case_data.get('data_type')
        if variable in header:
            headerlist=headersvariable.split(",")
            header=header%(tuple(headerlist))
        if variable in data:
            datalist=datavariable.split(",")
            data=data%(tuple(datalist))
        if method=='post':
            res = requests.post(url=url,headers=json.loads(header),data=json.dumps(json.loads(data)))
            log_case_info(case_name, url, data,res.status_code,res.elapsed.total_seconds(),res.text)
            res_text=res.text
        elif method=='get':
            res = requests.get(url=url,headers=json.loads(header),params=json.loads(data))
            log_case_info(case_name, url, data,res.status_code,res.elapsed.total_seconds(),res.text)
            res_text=res.text
        elif method=='put':
            res = requests.put(url=url,headers=json.loads(header),data=json.dumps(json.loads(data)))
            log_case_info(case_name, url, data,res.status_code,res.elapsed.total_seconds(),res.text)
            res_text=res.text
        elif method=='delete':
            res = requests.delete(url=url,headers=json.loads(header),data=json.dumps(json.loads(data)))
            log_case_info(case_name, url, data,res.status_code,res.elapsed.total_seconds(),res.text)
            res_text=res.text

        return res_text






        # if method.upper() == 'GET':   # GET类型请求
        #     res = requests.get(url=url, params=json.dumps(data))
        #
        # elif data_type.upper() == 'FORM':   # 表单格式请求
        #     res = requests.post(url=url, data=json.loads(data), headers=json.loads(headers))
        #     log_case_info(case_name, url, data, expect_res, res.text)
        #     self.assertEqual(res.text, expect_res)
        # else:
        #     res = requests.post(url=url, json=json.loads(data), headers=json.loads(headers))   # JSON格式请求
        #     log_case_info(case_name, url, data, json.dumps(json.loads(expect_res), sort_keys=True),
        #                   json.dumps(res.json(), ensure_ascii=False, sort_keys=True))
        #     self.assertDictEqual(res.json(), json.loads(expect_res))