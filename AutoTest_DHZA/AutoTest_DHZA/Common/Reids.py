import redis
import ast

class Redis:
    def __init__(self):
        self.pool=redis.ConnectionPool(host='172.16.3.14',port=6379,db=0,max_connections=1000)
        self.r = redis.Redis(connection_pool=self.pool)

    def get_register_code(self,phone):
        key='sms_register_test_'+str(phone)
        code=self.r.get(key)
        code=code.decode()
        return code

    def get_reset_code(self,phone):
        key='sms_reset_test_'+str(phone)
        code=self.r.get(key)
        code=code.decode()
        return code

    def get_uuid_key(self,UUID):
        key='verifyCode_'+UUID
        code=self.r.get(key)
        code=code.decode()
        code=ast.literal_eval(code)
        code=code[1].get("code")
        return code
