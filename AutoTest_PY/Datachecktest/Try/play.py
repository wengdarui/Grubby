import requests
import os
import random
import time
import json
import string

# 英雄的名字json

# url = 'http://pvp.qq.com/web201605/js/herolist.json'
#
#
# head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
# response = requests.get(url, headers=head)
# hero_list = response.json()
# print(hero_list)
#
# # 提取英雄名字和数字
# hero_name=list(map(lambda x:x['cname'], hero_list))
#
# hero_number=list(map(lambda x:x['ename'], hero_list))
#
# print(hero_name)
# print(hero_number)

# money_list=[]
# allmoney=15
#
#
# def money():
#     money=random.uniform(0.5,3.5)
#     money=(round(money,2))
#     money_list.append(money)
#
#
# def four_money():
#     for i in range(len('小熊牛皮')):
#         money()
#
# while 1:
#     four_money()
#     summoney=sum(money_list)
#     summoney=(round(summoney,2))
#     print('和%s'%summoney)
#     lastmoney=allmoney-summoney
#     if 0.5<=lastmoney<= 3.5:
#         lastmoney=(round(lastmoney,2))
#         money_list.append(lastmoney)
#         break
#     else:
#         money_list.clear()
#
# time.sleep(5)
# print(money_list)



# seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
# sa = []
# for i in range(8):
#     sa.append(random.choice(seed))
# salt = ''.join(sa)
#
# print(salt)
# def is_ip(ip):
#     num_list = ip.split(".")
#     for num in num_list:
#         if not num.isdigit() or not 0 <= int(num) <=255:
#             return False
#     return True
#
# print(is_ip("101.1.0.201"))


# def  check_ipv4(str):
#     ip = str.strip().split(".")
#     return False if len(ip) != 4 or False in map(lambda x:True if x.isdigit() and 0<= int(x) <= 255 else False, ip) else True
#
#
# print(check_ipv4("101.1.0.201"))


# res = requests.post("http://www.tuling123.com/openapi/api?key=ec961279f453459b9248f0aeb6600bbe&info=怎么又是你")
# print(res.text) # 输出为一行文本
# res_dict = res.json() # 将响应转为json对象（字典）等同于`json.loads(res.text)`
# print(json.dumps(res_dict, indent=1, sort_keys=True, ensure_ascii=False)) # 重新转为文本



# res = requests.get("https://www.baidu.com")
# print(res.status_code, res.reason) # 200 OK
# # print(res.text) # 文本格式，有乱码
# # print(res.content) # 二进制格式
# # print(res.encoding) # 查看解码格式 ISO-8859-1
# # print(res.apparent_encoding) # utf-8
# res.encoding='utf-8' # 手动设置解码格式为utf-8
# print(res.text) # 乱码问题被解决
# print(res.cookies.items()) # cookies中的所有的项 [('BDORZ', '27315')]
# print(res.cookies.get("BDORZ")) # 获取cookies中BDORZ所对应的值 27315


# ran_str = ''.join(random.sample(string.ascii_letters +string.ascii_letters+ string.digits, random.randint(28,68)))
# ran_zw = ''.join(random.choice(['小胖', '东哥', '强哥']))
# new_str=ran_str+ran_zw
#
# print(ran_str)
# print(ran_zw)
# print(new_str)

data={}
data['clientId'] = 'client123'
data['topic'] = 'DH/test/#'
data['deviceId'] = ["tiger_dream_007"]
data=json.dumps(data)
print(data)