import requests
import json
import random
import os
import pandas as pd
import openpyxl

"""
get_ip();get_agent()
读取ip_list，agent_list 文件，随机返回一个值
get_toutiao_info()
获取头条数据
data_to_file
写入数据到文件
"""
rq = requests

project_url = os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))
file_url = project_url+"/Download_file"

ip_list = file_url+"/ip_list.txt"
agent_list = file_url+"/agent_list.txt"

def get_ip():
    """
    :return:随机返回一个ip代理地址
    """
    with open(ip_list,"r") as f:
        iplist =f.readlines()
    random_ip = iplist[random.randint(0, len(iplist)-1)]
    return random_ip

def get_agent():
    """
    :return:随机返回一个agent参数
    """
    with open(agent_list,"r") as f:
        agentlist =f.readlines()
    random_agent = agentlist[random.randint(0, len(agentlist)-1)]
    random_agent = random_agent.replace("\n","")
    return random_agent



# 用户代理
headers = {
    "User-Agent": get_agent()
}

# ip代理
proxies = {
    "url": get_ip()
}

def get_toutiao_info():
    """
    :return:返回json格式的data
    """
    response = rq.get("https://www.toutiao.com/api/pc/feed/"
                      "?max_behot_time=1569679968&"
                      "category=__all__&utm_source=toutiao"
                      "&widen=1&tadrequire=true"
                      "&as=A135ED480F17A6C&cp=5D8FE71AD6CCBE1"
                      "&_signature=GCGQshAYRbNPFtjpx5sC9RghkK",
                      headers=headers,
                      proxies=proxies)
    response_info =json.loads(response.text)
    #判断返回的message是成功还是失败，失败则重新获取随机代理重新请求
    if response_info.get("message") == "error":
        get_toutiao_info()
    elif response_info.get("message") == "success":
        global data_json
        data_json = response_info.get("data")
    return data_json

def data_to_file():
    """
    :return:将json格式的数据，写入文件
    """
    data_json = get_toutiao_info()
    print(data_json,type(data_json))
    for i in range(len(data_json)):
        data_file = data_json[i]
        with open("toutiao_info.json","a+",encoding='utf-8') as f:  #如果ensure_ascii=False 还是报错的话加上编码指定
            json.dump(data_file,f,ensure_ascii=False)
            f.write("\n")

# data_to_file()

data_json = pd.read_json("toutiao_info.json",lines=True)
data_json.to_excel("toutiao.xlsx",encoding='utf-8') #若果写入到excel的数据出现乱码，加上编码指定

