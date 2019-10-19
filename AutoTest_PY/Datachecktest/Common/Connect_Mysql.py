from Common import Read_config
import configparser
import time
import os
import pymysql
import datetime

proDir = os.path.split(os.path.realpath('E:\AutoTest_PY\Datachecktest\config.ini'))[0]
configpath = os.path.join(proDir,'config.ini')

#创建实例化对象
cf=Read_config.ReadConfig()

#获取参数
host = cf.get_database('host')
root = cf.get_database('username')
pwd = cf.get_database('password')
db = cf.get_database('database')
port = cf.get_database('port')
port1 =int(port)


# DB = pymysql.connect(host,root,pwd,db,port=port1)

# #创建游标对象
# cursor = DB.cursor()
class DB:
    def __init__(self):
        self.conn = pymysql.connect(host,root,pwd,db,port=port1)
        self.cur = self.conn.cursor()
    def __del__(self): # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
    def connect0(self,sql):
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def connect1(self,sql,parameter):
        self.cur.execute(sql,(parameter))
        results = self.cur.fetchall()
        return results
    def connect2(self,sql,parameter,parameter1):
        self.cur.execute(sql,(parameter,parameter1))
        results = self.cur.fetchall()

        return results
    def connect3(self,sql,parameter,parameter1,parameter2):
        self.cur.execute(sql,(parameter,parameter1,parameter2))
        results = self.cur.fetchall()
        return results



if __name__ == '__main__':
    DB.connect0
    DB.connect1
    DB.connect2
    DB.connect3

