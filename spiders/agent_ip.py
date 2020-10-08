from bs4 import BeautifulSoup
import requests
import random


# 格式化ip
def get_proxy(agent_ip):
    proxy_ip = 'http://' + agent_ip
    proxy_ips = 'https://' + agent_ip
    proxies = {'https': proxy_ips, 'http': proxy_ip}
    return proxies


# 从网站上获取ip
def get_ip_list(url, headers):
    ip_list = []
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    url_list = soup.find_all('tr')
    print(len(url_list))
    for i in range(2, len(url_list)):
        line = url_list[i].find_all('td')
        ip = line[0].text
        port = line[1].text
        address = ip + ':' + port
        ip_list.append(address)
    return ip_list


# 得到一个proxies
def get_ip(url, headers):
    agent_ip = random.choice(get_ip_list(url, headers))
    proxies = get_proxy(agent_ip)
    print(proxies)
    return proxies
