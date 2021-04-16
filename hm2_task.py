import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy


def my_vacancy(vacancy, header, proxy, area=0):
    vacancy = vacancy.replace(' ', '+')
    url = 'https://nn.hh.ru/search/vacancy/'
    param = {
        "text": f'{vacancy}',
        "area": f'{area}',  # area 1 - Moscow, 66 - Nizghnii Novgorod
        "order_by": 'relevance',
        "items_on_page": '50',
        "page": "0"
    }
    req = requests.get(url, headers=header, params=param, proxies=proxy)
    return req

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

proxies = {
    'http': f'{FreeProxy().get()}'
    }

req = my_vacancy('data engineer', headers, proxies, 0)
soup = bs(req.text, "html.parser")

item_list = soup.find(attrs={"class": "vacancy-serp"})
items = soup.find_all(attrs={"class": "") # почему тут пусто???


print()

items_info = []
for item in item_list.children:
    info = {}
    a = item.find("a", attrs={"class": "bloko-link"})
    if a is not None:
        info['vacance'] = a.attrs['href']

print()