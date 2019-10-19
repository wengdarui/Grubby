from Common import Read_config
from Common import encryption
import logging
from Common import Log
import configparser
import time
import os
import pymysql
import datetime


#创建实例化对象
cf=Read_config.ReadConfig()
bc=encryption.Encryption

#获取参数
host = cf.get_database('host')
root = cf.get_database('username')
pwd = cf.get_database('password')
db_user = cf.get_database('database_user')
db_enterprise =cf.get_database('database_enterprise')
db_en = cf.get_database('database_enterprise')
port = cf.get_database('port')
port1 =int(port)
user_password = str(cf.get_userdatainfo('not_exist_pwd'))
#加密
newpassword=bc.bcrypt_en(user_password)


# DB = pymysql.connect(host,root,pwd,db,port=port1)

# #创建游标对象
# cursor = DB.cursor()
class DB_user:
    def __init__(self):
        self.conn = pymysql.connect(host,root,pwd,db_user,port=port1)
        self.cur = self.conn.cursor()
    def __del__(self): # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
    def query(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def commit(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))
    def check_user(self,phone):
        result = self.query("select id from tb_user where phone={}".format(phone))
        return True if result else False

    def del_user(self, phone):
        self.commit("delete from user where phone='{}'".format(phone))

    def clear_data(self, sql, parameter):
        try:
            self.cur.execute(sql,(parameter))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))

    def updata_data(self, sql, parameter):
        try:
            self.cur.execute(sql,(parameter))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))

    def create_user(self,username,phone):
        id=self.query("SELECT id from tb_user ORDER BY id DESC LIMIT 1;")
        id=id[0][0]+1
        self.commit("INSERT INTO `tb_user`(id,`name`,phone,`password`) VALUES({0},'{1}',{2},'{3}');".format(id,username,phone,newpassword))

    def query1(self,sql,parameter):
        self.cur.execute(sql,(parameter))
        results = self.cur.fetchall()
        return results

    def query2(self,sql,parameter,parameter1):
        self.cur.execute(sql,(parameter,parameter1))
        results = self.cur.fetchall()
        return results

    def query3(self,sql,parameter,parameter1,parameter2):
        self.cur.execute(sql,(parameter,parameter1,parameter2))
        results = self.cur.fetchall()
        return results

class DB_enterprise:
    def __init__(self):
        self.conn = pymysql.connect(host,root,pwd,db_enterprise,port=port1)
        self.cur = self.conn.cursor()
    def __del__(self): # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
    def query(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def commit(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))

    def check_user(self,phone):
        result = self.query("select id from tb_user where phone={}".format(phone))
        return True if result else False

    def del_user(self, phone):
        self.commit("delete from user where phone='{}'".format(phone))

    def clear_data(self, sql, parameter):
        try:
            self.cur.execute(sql,(parameter))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))

    def updata_data(self, sql, parameter):
        try:
            self.cur.execute(sql,(parameter))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(str(e))
    # def add_application(self, user_id):
    #     self.commit("INSERT INTO`application`(apply_type,company_id,user_id) VALUES({0},'{1}',{2});".format('1','56',user_id))


    def query1(self,sql,parameter):
        self.cur.execute(sql,(parameter))
        results = self.cur.fetchall()
        return results

    def query2(self,sql,parameter,parameter1):
        self.cur.execute(sql,(parameter,parameter1))
        results = self.cur.fetchall()
        return results

    def query3(self,sql,parameter,parameter1,parameter2):
        self.cur.execute(sql,(parameter,parameter1,parameter2))
        results = self.cur.fetchall()
        return results





if __name__ == '__main__':
    DB_user.connect0
    DB_user.connect1
    DB_user.connect2
    DB_user.connect3

