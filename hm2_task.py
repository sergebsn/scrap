import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy
import pandas as pd



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


req = my_vacancy('повар', headers, proxies, 0)
soup = bs(req.text, "html.parser")

item_list = soup.find(attrs={"class": "vacancy-serp"})
items = item_list.findChildren(recursive=False)

items_info = []
for item in items:
    info = {}
    try:
        a = item.find("a")
        info['Link'] = a.attrs["href"]
        info['Name'] = a.get_text()
        #info['zp0'] = a.find(attrs={"data-qa":"vacancy-serp__vacancy-compensation"}).text
    except Exception as e:
        print(e)

df = pd.DataFrame([info])
df.to_csv("df.csv")
