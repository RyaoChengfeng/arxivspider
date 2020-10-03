import re
import requests
from bs4 import BeautifulSoup

url_arvix = "https://arxiv.org/list/cs.AI/pastweek?skip=0&show=165#item144"
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

    # 获得论文信息
    r_title0 = re.compile(r'<h1 class="title mathjax"><span class="descriptor">Title:</span>(.*?)</h1>')
    r_title = re.findall(r_title0, doc)[0]

    r_author0 = re.compile(r'<div class="authors">(.*?)</div>')
    r_author1 = re.findall(r_author0, doc)[0]
    r_author2 = re.findall(r'<a>(.*?)</a>', r_author1)[0]
    for r_author in r_author2:
        r_author = r_author.replace()


    r_time0 = re.compile(r'Submitted on (.*?)]')
    r_time = re.findall(r_time0, doc)[0]

    # 将得到的数据存入数据库
    # ..........

    # 控制爬取的论文量


# 下载功能
def download_pdf(url):
    pdf_file = requests.get(url, headers=headers)
    fileroute = 'Artificial Intelligence/' + number + '.pdf'
    with open(fileroute, 'wb') as f:
        f.write(pdf_file.content)


# 下载各论文到Artificial Intelligence
for number in r_number_list:
    url_pdf = "https://arxiv.org" + number
    download_pdf(url_pdf)
