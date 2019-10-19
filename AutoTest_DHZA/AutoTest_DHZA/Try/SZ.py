import json
import re

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
    pattern = re.compile(r'<dd>.*?<i.*?board-index-.*?>(.*?)</i>.*?data-src="(.*?)".*?title="(.*?)".'
                         r'*?主演：(.*?)</p>.*?上映时间：(.*?)</p>.*?integer">(.*?)</i>.*?fraction">'
                         r'(.*?)</i>.*?</dd>', re.S)

    html1 = html.replace('\n','').replace('\t','').replace(' ','')
    for i in re.findall(pattern, html):
            yield {
                'index': i[0],
                'image': i[1],
                'title': i[2],
                'actor': i[3].strip()[3:],
                'time': i[4].strip()[5:],
                'score': i[5] + i[6]
            }



def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main():
    url = "https://maoyan.com/board"
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        # write_to_file(item)

if __name__ == '__main__':
    main()