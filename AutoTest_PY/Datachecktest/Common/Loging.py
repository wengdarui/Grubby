import requests
import ast
from Common import Read_config

cf=Read_config.ReadConfig()
#app
login_url_app = cf.get_httpurl('login_url')
login_header = ast.literal_eval(cf.get_httpurl('login_header'))
timeout= float(cf.get_http('timeout'))
login_content_33 = ast.literal_eval(cf.get_httpurl('login_content33'))
login_content_3x = ast.literal_eval(cf.get_httpurl('login_content3x'))


#大智
login_url_dz = cf.get_httpsurl('login_url')
login_header = ast.literal_eval(cf.get_httpsurl('login_header'))
login_data = ast.literal_eval(cf.get_httpsurl('login_data'))
json={
	"minproId": 1,
	"plat": 1,
	"openId": "o5kFK5NpG2mYMsvz2yHJ3eUtQ9U8",
	"invitedCode": "",
	"codeNo": 0,
	"username": "WDR",
	"headImage": "https://wx.qlogo.cn/mmopen/vi_32/ppIfbwt83qcMtSvVmd3MPNq1jbVqnfHatxo42TbxIoX3wP8hz1DUh9qUZtIbCyxyjZVjflmvSFP3GrKU8JOfbw/132",
	"gender": 1
}



def login_3_3():
    lg=requests.get(login_url_app,params=login_content_33,headers=login_header)
    request=(lg.json())
    token=(request.get('data').get('token'))
    return token,request

def login_3_x():
    lg=requests.get(login_url_app,params=login_content_3x,headers=login_header)
    request=(lg.json())
    token=(request.get('data').get('token'))
    return token,request

def login_DZ():
    lg=requests.post(login_url_dz,data=login_data,timeout=timeout)
    request=(lg.json())
    token=(request.get('data').get('token'))
    return token,request



if __name__ == '__main__':
    login_3_3()
    login_3_x()
    login_DZ()



