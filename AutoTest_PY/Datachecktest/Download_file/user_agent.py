import requests
import json


rq = requests
"""
请求user-agent网站获取的数据
获取浏览器类型列表
读取拼接写入文件
"""
def get_agent_list():
    url = "https://fake-useragent.herokuapp.com/browsers/0.1.11"
    response = rq.get(url)
    rs = json.loads(response.text)
    browser_list = rs['browsers'].keys()
    for i in browser_list:
        agent_list = rs['browsers'][i]
        for a in agent_list:
            with open("agent_list.txt", "a+") as f:
                f.write(a)
                f.write("\n")

get_agent_list()