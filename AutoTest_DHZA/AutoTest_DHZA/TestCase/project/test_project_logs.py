import  time
import datetime
import json
import re
from Common import encryption
from Common import Reids
from Common import DB
from Common import Read_config
from Common.BaseCase import BaseCase

#数据准备
cf=Read_config.ReadConfig()
db=DB.DB_enterprise()
re=Reids.Redis()
logintoken=cf.get_userdatainfo('logintoken')
worksurfaceid=cf.get_project('worksurfaceid')
daytime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
utctime=datetime.datetime.utcnow().isoformat()

class test_project_logs(BaseCase):
    def test_add_projectlogs(self): #添加施工日志（utc时间）
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data_value=daytime+','+worksurfaceid+','+daytime+','+projectid+','+daytime
        data=self.get_case_data("test_add_projectlogs")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('200',check)
        request = json.loads(check)
        projectlogsid=request.get('data')
        cf.set_project('projectlogsid',str(projectlogsid))

    def test_get_worksurfacearea(self): #获取作业面列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_worksurfacearea")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('中和雄起兔',check)

    def test_get_categorylist(self): #获取施工日志类别列表
        data=self.get_case_data("test_get_categorylist")
        check=self.send_request(data,headersvariable=logintoken)
        self.assertIn('水电',check)

    def test_get_projectlogslist(self): #获取施工日志列表
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data=self.get_case_data("test_get_projectlogslist")
        check=self.send_request(data,headersvariable=logintoken,datavariable=projectid)
        self.assertIn('开关面板安装',check)

    def test_get_projectlogsinfo(self): #获取施工日志详情
        time.sleep(2)
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        projectlogsid=cf.get_project('projectlogsid')
        data_value=projectlogsid+','+projectid
        data=self.get_case_data("test_get_projectlogsinfo")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('开关面板安装',check)

    def test_update_projectlogs(self): #更新施工日志（utc时间）
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        projectlogsid=cf.get_project('projectlogsid')
        data_value=daytime+','+projectlogsid+','+worksurfaceid+','+daytime+','+projectid+','+daytime
        data=self.get_case_data("test_update_projectlogs")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('success',check)

    def test_get_worksurfacecolumn(self): #获取作业面信息（包含考勤，施工日志）
        cf=Read_config.ReadConfig()
        projectid=cf.get_project('projectid')
        data_value=projectid+','+worksurfaceid+','+daytime
        data=self.get_case_data("test_get_worksurfacecolumn")
        check=self.send_request(data,headersvariable=logintoken,datavariable=data_value)
        self.assertIn('开关面板安装',check)