import re
import requests
import os
from bs4 import BeautifulSoup

url_arvix = "https://arxiv.org/list/cs.AI/pastweek?skip=0&show=165"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

page = requests.get(url_arvix, headers=headers)
html = page.text
r_number = re.compile(r'<a href="/abs/(.*?)" title="Abstract">')
r_number_list = re.findall(r_number, html)
print(r_number_list)


# 下载功能
def download_pdf(url):
    pdf_file = requests.get(url, headers=headers, stream=True)
    # stream=True保持流的开启,直到流的关闭
    file_dir = 'Artificial Intelligence'
    pdf_name = 'arXiv:' + number
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(os.path.join(file_dir, pdf_name), 'wb') as f:
        f.write(pdf_file.content)


n = 0
# 下载各论文到Artificial Intelligence
for number in r_number_list:
    url_pdf = "https://arxiv.org/" + number
    print(url_pdf)
    download_pdf(url_pdf)
    n += 1
    if n == 3:
        break
