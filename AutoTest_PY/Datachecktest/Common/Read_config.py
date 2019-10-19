import os
import configparser
import ast
import codecs


proDir = os.path.split(os.path.realpath('D:\Test\AutoTest_PY\Datachecktest\config.ini'))[0]
configpath = os.path.join(proDir,'config.ini')


# # #创建实例化对象
# cf = configparser.ConfigParser()
# cf.read(configpath,encoding='UTF8')

class ReadConfig:
    def __init__(self):
        # fd = open(configpath)
        # data = fd.read()
        #
        # #  remove BOM
        # if data[:3] == codecs.BOM_UTF8:
        #     data = data[3:]
        #     file = codecs.open(configpath, "w")
        #     file.write(data)
        #     file.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configpath,encoding='UTF8')

    def get_database(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_schoolid(self, name):
        value = self.cf.get("schoolId", name)
        return value

    def get_httpurl(self, name):
        value = self.cf.get("HTTPURL", name)
        return value

    def get_httpsurl(self, name):
        value = self.cf.get("HTTPSURL", name)
        return value

    def get_Android_OPPO(self, name):
        value = self.cf.get("Android_OPPO", name)
        return value


