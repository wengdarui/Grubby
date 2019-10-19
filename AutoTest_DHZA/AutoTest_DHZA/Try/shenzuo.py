import json
import re
import bs4
import requests
from requests.exceptions import RequestException

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/76.0.3809.132 Safari/537.36"
headers = {"User-Agent": user_agent}


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    sp = bs4.BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
    date = sp.find('div', id='app')
    id= date.find_all('i')
    img= date.find_all('img')
    p = date.find_all('p')
    ID= re.findall('board-index-(.*?)"', str(id))
    title=re.findall('title="(.*?)"', str(p))
    imgurl=re.findall('data-src="(.*?)"', str(img))
    actor=re.findall('主演：(.*)', str(p))
    time=re.findall('上映时间：(.*?)</p>', str(p))
    score1=re.findall('integer">(.*?)<', str(p))
    score2=re.findall('fraction">(.*?)<', str(p))

    for i in range(0,len(ID)):
        yield{
            'index': str(ID[i]),
            'image': imgurl[i],
            'title': title[i],
            'actor': actor[i],
            'time':  time[i],
            'score': score1[i] + score2[i]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main():
    url = "https://maoyan.com/board"
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    main()