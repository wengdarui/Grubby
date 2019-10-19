#!usr/bin/env python
# encoding:utf-8

import urllib.request
import bs4
import re
from urllib import error
import time
import datetime
import ssl

#拼接请求链接以及获取网页内容
def getHtml(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    headers = {"User-Agent":user_agent}
    try:
        request = urllib.request.Request(url,headers=headers)
        if request._data== None:
            html='没有内容'
        else:
            response = urllib.request.urlopen(request)
            html = response.read()
    except error.URLError as e:
        return ('错误信息：%s'%e)
    return html



# 格式化网页内容
def parse(url):
    html_doc = getHtml(url)
    sp = bs4.BeautifulSoup(html_doc, 'html.parser', from_encoding="utf-8")
    return sp

# 根据最新更新时间判断是否有更新章节
def check_update(url):
    update = parse(url).find('div', id='info')
    uptime=update.find_all('p')[2].get_text()
    uptime_new=re.findall(r"最后更新：(.+?) ",uptime)


    localtime = datetime.datetime.now().timetuple()
    localtime_format=str(localtime.tm_mon)+'/'+str(localtime.tm_mday)+'/'+str(localtime.tm_year)

    if uptime_new == localtime_format:
        books_info = {}
        books_info['name'] = (update.find_all('a')[3].get_text())
        books_info['url'] = 'https://www.biquge.cc/html/139/139744/' + update.find_all('a')[3].get('href')
        return books_info
    else:
        error_info='！！！暂无更新！！！'
        return error_info

#获取具体章节内容并下载
def download_txt(url):
    time.sleep(1)
    download_url=check_update(url).get('url')
    download_html=parse(download_url)
    download_content=download_html.find('div', id='content')
    text_all=download_content.get_text()
    text_all=text_all.replace(u'\u3000', u'').replace(u'\xa0', u'')
    text_all=text_all.split('。')
    try:
        FJwd=open("E:\Download\FJwd.txt", "a+",encoding="utf-8")
        FJwd.write(check_update(url).get('name') +'\n' )
        for i in range(len(text_all)):
            FJwd.write(text_all[i] + '\n')
        return ('最新章节写入成功')
    except error as e:
        return ('错误信息：%s'%e)
    finally:
        FJwd.close()


if __name__ == '__main__':
    url='https://www.biquge.cc/html/139/139744/'
    try:
        book = download_txt(url)
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%s"%e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s"%e.reason)
    finally:
        print('%s'%book)












