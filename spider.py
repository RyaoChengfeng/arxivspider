import re
import requests
import os
from bs4 import BeautifulSoup

url_arvix = "https://arxiv.org/list/cs.AI/pastweek?skip=0&show=165"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

# 获取每个论文代号
page = requests.get(url_arvix, headers=headers)
html = page.text
r_number = re.compile(r'<a href="/abs/(.*?)" title="Abstract">')
r_number_list = re.findall(r_number, html)

# 进入论文内部爬取
for number in r_number_list:
    url_doc = 'https://arxiv.org/abs/' + number
    doc = requests.get(url_doc, headers=headers)
    doc = doc.text

    number_id = 'arXiv:' + number  # 论文序号

    # 信息提示
    print('正在爬取论文: %s' % number_id)

    soup = BeautifulSoup(doc, 'lxml')
    # 获得论文信息
    r_title0 = re.compile(r'<h1 class="title mathjax"><span class="descriptor">Title:</span>(.*?)</h1>')
    r_title = re.findall(r_title0, doc)[0]  # 论文标题

    div = soup.find_all(attrs={'class': 'authors'})[0]
    authors = div.find_all(name='a')
    for author in authors:
        author = author.string  # 论文作者

    r_time0 = re.compile(r'Submitted on (.*?)]')
    r_time = re.findall(r_time0, doc)[0]  # 论文时间

    # 将得到的数据存入数据库
    # ..........

    # 控制爬取的论文量
    # # i = 0
    # if i = n:
    #     break


# 下载功能 (失效)
def download_pdf(url):
    pdf_file = requests.get(url, headers=headers, stream=True)
    # stream=True保持流的开启,直到流的关闭
    file_dir = 'Artificial Intelligence'
    pdf_name = 'arXiv:' + number
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(os.path.join(file_dir, pdf_name), 'wb') as f:
        f.write(pdf_file.content)


# 下载各论文到Artificial Intelligence
for number in r_number_list:
    url_pdf = "https://arxiv.org/" + number  # 下载地址
    print('开始下载论文：arXiv:%s' % number)
    download_pdf(url_pdf)
