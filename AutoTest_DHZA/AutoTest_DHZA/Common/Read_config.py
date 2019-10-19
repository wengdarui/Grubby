import os
import configparser
import ast
import codecs


# proDir = os.path.split(os.path.realpath('D:\Test\AutoTest_DHZA\AutoTest_DHZA\/'))[0]
# configpath = os.path.join(proDir,'config.ini')
proDir = os.path.dirname(os.path.abspath(__file__))
proDir1=os.path.dirname(os.path.abspath(proDir))
configpath = os.path.join(proDir1,'config.ini')



# # #创建实例化对象
# cf = configparser.ConfigParser()
# self.cf.read(configpath,encoding='UTF8')

class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath,encoding='UTF8')

    def get_database(self,name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_http(self,name):
        value = self.cf.get("HTTP", name)
        return value

    def get_userdatainfo(self,name):
        value = self.cf.get("User_data_info", name)
        return value

    def set_userdatainfo(self,name,value):
        cf = configparser.ConfigParser()
        cf.read(configpath,encoding='UTF8')
        cf.set("User_data_info",name,value)
        try:
            with open(configpath,"w+") as f:
                cf.write(f)
        except ImportError:
            pass

    def get_enterpriseinfo(self,name):
        value = self.cf.get("Enterprise_info", name)
        return value

    def set_enterpriseinfo(self,name,value):
        cf = configparser.ConfigParser()
        cf.read(configpath,encoding='UTF8')
        cf.set("Enterprise_info",name,value)
        try:
            with open(configpath,"w+") as f:
                cf.write(f)
        except ImportError:
            pass

    def get_departmentinfo(self,name):
        value = self.cf.get("Department_info", name)
        return value

    def set_departmentinfo(self,name,value):
        cf = configparser.ConfigParser()
        cf.read(configpath,encoding='UTF8')
        cf.set("Department_info",name,value)
        try:
            with open(configpath,"w+") as f:
                cf.write(f)
        except ImportError:
            pass

    def get_employeeinfo(self,name):
        value = self.cf.get("Employee_info", name)
        return value

    def set_employeeinfo(self,name,value):
        cf = configparser.ConfigParser()
        cf.read(configpath,encoding='UTF8')
        cf.set("Employee_info",name,value)
        try:
            with open(configpath,"w+") as f:
                cf.write(f)
        except ImportError:
            pass

    def get_project(self,name):
        value = self.cf.get("Project_info", name)
        return value

    def set_project(self,name,value):
        cf = configparser.ConfigParser()
        cf.read(configpath,encoding='UTF8')
        cf.set("Project_info",name,value)
        try:
            with open(configpath,"w+") as f:
                cf.write(f)
        except ImportError:
            pass

    def get_testsrite(self,name):
        value = self.cf.get("TestSuite", name)
        return value


    def get_email(self,name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_Android_OPPO(self,name):
        value = self.cf.get("Android_OPPO", name)
        return value


# if __name__ == '__main__':
