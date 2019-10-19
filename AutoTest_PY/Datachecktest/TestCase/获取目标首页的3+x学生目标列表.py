#!usr/bin/env python
# encoding:utf-8

import requests
import json


login_url='http://testapi.ubzyw.com/v1/rest/login/doLogin'
login_content={'password':123456,'phoneOrEmail':13020000371}
login_header={'UB_UserAgent_deviceOS':'ios'}
login=requests.get(login_url,params=login_content,headers=login_header)

request=(login.json())
token=(request.get('data').get('token'))

print(token)

getUserAim_url='http://testapi.ubzyw.com/v1/rest/studentaim/getUserAim'
getUserAim_content={'coverageFlag':1,'groupId':4,'UB_UserAgent_appUserAuthToken':token}
getUserAim=requests.get(getUserAim_url,params=getUserAim_content)

getUserAim_request=(getUserAim.json())
print(getUserAim_request)
schoolIds_two1=(getUserAim_request['data']['schoolNum'][0]['schoolIds'])
school_1=(getUserAim_request['data']['schoolNum'][1]['schoolIds'])
print(schoolIds_two1)
print(school_1)
