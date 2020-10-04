import re
import requests
import os
from bs4 import BeautifulSoup
import random
from db import get_db
from flask import g, flash, render_template
import pymysql

url_arvix = "https://arxiv.org/list/cs.AI/pastweek?skip=0&show=165"
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]

headers = {'User-Agent': random.choice(user_agent)}


# 获取每个论文代号
def get_number():
    page = requests.get(url_arvix, headers=headers)
    html = page.text
    r_number = re.compile(r'<a href="/abs/(.*?)" title="Abstract">')
    r_number_list = re.findall(r_number, html)
    return r_number_list


# 进入论文内部爬取
def get_msg():
    messages = []  # 总数据
    _ = 1
    r_number_list = get_number()
    for number in r_number_list[8:20]:
        url_doc = 'https://arxiv.org/abs/' + number
        doc = requests.get(url_doc, headers=headers)
        doc = doc.text

        # 论文序号
        number_id = 'arXiv:' + number

        # 信息提示
        print('正在爬取论文: %s' % number_id)

        soup = BeautifulSoup(doc, 'lxml')
        # 获得论文信息

        # 论文标题
        r_title0 = re.compile(r'<h1 class="title mathjax"><span class="descriptor">Title:</span>(.*?)</h1>')
        r_title = re.findall(r_title0, doc)[0]
        # 论文作者
        div = soup.find_all(attrs={'class': 'authors'})[0]
        author_list = div.find_all(name='a')
        authors = ''
        for author in author_list:
            author = author.string
            if author == author_list[0].string:
                authors = author
            else:
                authors = authors + ',' + author
        # 论文时间
        r_time0 = re.compile(r'Submitted on (.*?)]')
        r_time = re.findall(r_time0, doc)[0]
        # 论文类别
        sbj = soup.find_all('span', class_='primary-subject')[0]
        sbj = str(sbj.string)
        # 下载地址
        url_pdf = "https://arxiv.org/pdf/" + number + '.pdf'

        messages.append((r_title, number_id, authors, r_time, sbj, url_pdf))

    print('爬取完成')
    return messages


# 下载功能
def download_all_pdf(url, number):
    pdf_file = requests.get(url, headers=headers, stream=True)
    # stream=True保持流的开启,直到流的关闭
    file_dir = 'Artificial Intelligence'
    pdf_name = number + '.pdf'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    fileroute = os.path.join(file_dir, pdf_name)
    with open(fileroute, 'wb') as f:
        for chunk in pdf_file.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


# 下载各论文到Artificial Intelligence
def get_all_doc():
    r_number_list = get_number()
    for number in r_number_list:
        url_pdf = "https://arxiv.org/pdf/" + number + '.pdf'
        print('开始下载论文：arXiv:%s' % number)
        download_all_pdf(url_pdf, number)


