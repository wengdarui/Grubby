import json
import time
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
logintoken=cf.get_userdatainfo('logintoken')


class test_enterprise_announcement(BaseCase):  #企业公告
    def test_enterprise_addannouncement(self): #添加企业公告
        data=self.get_case_data("test_enterprise_addannouncement")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('200',check)
        request = json.loads(check)
        ggid = str(request.get('data'))
        cf.set_enterpriseinfo('announcementid',ggid)

    def test_enterprise_getannouncement(self): #查看企业公告详情
        time.sleep(2)
        cf=Read_config.ReadConfig()
        ggid=cf.get_enterpriseinfo('announcementid')
        data=self.get_case_data("test_enterprise_getannouncement")
        check=self.send_request(data,headersvariable=logintoken,datavariable=ggid)
        self.assertIn('番茄炒蛋、红烧肉、鱼香肉丝',check)

    def test_enterprise_announcementlist(self): #企业公告列表
        data=self.get_case_data("test_enterprise_announcementlist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('200',check)

    def test_enterprise_updateannouncement(self): #更新企业公告
        time.sleep(2)
        cf=Read_config.ReadConfig()
        ggid=cf.get_enterpriseinfo('announcementid')
        data=self.get_case_data("test_enterprise_updateannouncement")
        check=self.send_request(data,headersvariable=logintoken,datavariable=ggid)
        self.assertIn('200',check)

    def test_enterprise_deleteannouncement(self): #删除企业公告
        time.sleep(2)
        cf=Read_config.ReadConfig()
        ggid=cf.get_enterpriseinfo('announcementid')
        data=self.get_case_data("test_enterprise_deleteannouncement")
        check=self.send_request(data,headersvariable=logintoken,datavariable=ggid)
        self.assertIn('200',check)

