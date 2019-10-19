import requests
import re
import time

"""
请求ip代理网站前10个分页的数据，
正则提取ip；port并放到一个list里面
读取拼接写入文件

"""

rq = requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Host": "www.kuaidaili.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

}

def get_ip_list():
    for i in range(1,11):
        url ="https://www.kuaidaili.com/free/inha/"+str(i)+"/"
        time.sleep(2) #不想判断网页有没有返回直接等2s
        response=rq.get(url, headers=headers)
        rs = response.text
        ipre = re.compile('"IP">(.*?)</td>')
        portre = re.compile('"PORT">(.*?)</td>')
        ip_list = ipre.findall(rs)
        port_list = portre.findall(rs)
        ip_prot = [(i, p) for i, p in zip(ip_list, port_list)]
        for i in ip_prot:
            new_ip = "http://"+ i[0]+":"+i[1]
            with open("ip_list.txt", "a+") as f:
                f.write(new_ip)
                f.write("\n")



get_ip_list()








