
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:17:56 2019

@author: Smallkang94
"""

###############使用Xpath解析#################
import requests
from requests.exceptions import RequestException #导入异常处理模块
import json
from lxml import etree

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

#使用Xpath提取
def parse_one_page(html): 
    text_html = etree.HTML(html)  
    index = text_html.xpath('//i[contains(@class, "board-index")]/text()') 
    title = text_html.xpath('//p[@class="name"]/a/text()')
    actor = text_html.xpath('//p[@class="star"]/text()')
    time = text_html.xpath('//p[@class="releasetime"]/text()')
    integer = text_html.xpath('//p[@class="score"]/i[1]/text()') 
    fraction = text_html.xpath('//p[@class="score"]/i[2]/text()')
    for item in range(10):
        items = {'index':index[item],
                 'title':title[item].split(),
                 'actor':actor[item].strip()[3:] if len(actor[item]) > 3 else '',
                 'time':time[item].strip(),
                 'score':integer[item].strip() + fraction[item].strip()}
        print(items)
        write_to_file(items)

#写入文件    
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')#ensure_ascii参数为False,以保证输入结果为中文形式而不是Unicode编码。

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)  
    items = parse_one_page(html)

if __name__ == '__main__':
    for i in range(2):
        main(offset = i * 10)

###############使用BeautifulSoup解析#################
import requests
from bs4 import BeautifulSoup
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

#使用BeautifulSoup提取
def parse_one_page(html): 
    soup = BeautifulSoup(html, 'lxml')     
    index = soup.find_all(attrs={'class':"board-index"})
    title = soup.find_all(attrs={'class':"name"})
    actor = soup.find_all(attrs={'class':"star"})
    time = soup.find_all(attrs={'class':"releasetime"})
    integer = soup.find_all(attrs={'class':"integer"}) 
    fraction = soup.find_all(attrs={'class':"fraction"})
    for item in range(10):
        items = {'index':index[item].string,
                 'title':title[item].string.split(),
                 'actor':actor[item].string.strip()[3:] if len(actor[item].string) > 3 else '',
                 'time':time[item].string.strip(),
                 'score':integer[item].string.strip() + fraction[item].string.strip()}
        print(items)
        write_to_file(items)

#写入文件    
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')#ensure_ascii参数为False,以保证输入结果为中文形式而不是Unicode编码。

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)  
    items = parse_one_page(html)

if __name__ == '__main__':
    for i in range(1):
        main(offset = i * 10)


###############使用pyquery解析#################
import requests
from pyquery import PyQuery as pq
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

#使用pyquery提取
def parse_one_page(html): 
    doc = pq(html)   
    index = doc('.board-index').items()
    title = doc('.name').items()
    actor = doc('.star').items()
    time = doc('.releasetime').items()
    integer = doc('.integer').items()
    fraction = doc('.fraction').items()    
#    item = []
    for item in zip(index, title, actor, time, integer, fraction):
        yield({'index':item[0].text(),
             'title':item[1].text().split(),
             'actor':item[2].text().strip()[3:] if len(item[2].text()) > 3 else '',
             'time':item[3].text().strip(),
             'score':item[4].text().strip() + item[5].text().strip()})

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

