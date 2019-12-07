
import requests
import re
from requests.exceptions import RequestException #导入异常处理模块
import json

#抓取单页url
def get_one_page(url): 
    #添加请求头，模拟浏览器登录
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
    try:    
        response = requests.get(url, headers=headers) 
        if response.status_code == 200: 
            return response.text
    except RequestException:
        return response.status_code
#正则提取
def parse_one_page(html):    
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?<p.*?class="name">.*?<a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?"releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield({'index':item[0],
              'title':item[1].strip(),
              'actor':item[2].strip()[3:] if len(item[2]) > 3 else '',
              'time':item[3].strip(),
              'score':item[4].strip() + item[5].strip()})
#写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')#ensure_ascii参数为False,以保证输入结果为中文形式而不是Unicode编码。

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)    
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(2):
        main(offset = i * 10)

























