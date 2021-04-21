# import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy
import pandas as pd
import time
from pprint import pprint
# подключаем модуль MongoClient
from pymongo import MongoClient
MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "posts"


url = 'https://hh.ru/search/vacancy/'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
proxies = {
    'http': f'{FreeProxy().get()}'
}


# def get(url, headers, params):
#  req = requests.get(url, headers=headers, params=params, proxies=proxies)
# return req

# params = {
#        "clusters": "true",
#        "enable_snippets": "true",
#        "salary": {"st": "searchVacancy"},
#        "text": f'{vacancy}',
#        "showClusters": "true",
#        "page": 0,
#    }

def get_vacancy(url, vacancy, headers, proxies, page):
    params = {
        "clusters": "true",
        "text": f'{vacancy}',
        "showClusters": "true",
        "page": f'{page}',
    }
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return bs(r.text, "html.parser")


def get_vacancy_info(vacancy):
    items_info = []
    i = 0
    soup = get_vacancy(url, vacancy, headers, proxies, str(i))
    while True:
        items = soup.find_all(attrs={"class": "vacancy-serp-item"})
        # item_list = soup.find(attrs={"class": "vacancy-serp-item"})
        for item in items:
            info = {}
            a = item.find("a", attrs={"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
            info["vacancy"] = a.getText().replace(u"\xa0", " ")
            info["href"] = a.attrs["href"]
            info["web"] = url

            employer = item.find("a", attrs={"class": "bloko-link bloko-link_secondary",
                                             "data-qa": "vacancy-serp__vacancy-emloyer"})

            if employer is None:
                info["employer"] = ''
            else:
                info["employer"] = employer.getText().replace(u"\xa0", " ")

            salary = item.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

            if salary is not None:
                salary = salary.getText().replace(u"\xa0", " ")
                salary = salary.replace(u"\202f", " ")
                salary = salary.replace("-", " ")
                salary = salary.split()

                if salary[0] == 'от':
                    info["salary_min"] = salary[1]
                    info["salary_max"] = None
                    info["currency"] = salary[2]
                elif salary[0] == 'до':
                    info["salary_min"] = None
                    info["salary_max"] = salary[1]
                    info["currency"] = salary[2]
                else:
                    info["salary_min"] = salary[0]
                    info["salary_max"] = salary[1]
                    info["currency"] = salary[2]
                items_info.append(info)
            i += 1
            if soup.find(attrs={"class": "bloko-button", "data-qa": "pager-next"}) is None:
                break
            soup = get_vacancy(url, vacancy, headers, proxies, str(i))
        return items_info

# создаем функцию добавления вакансии в БД с проверкой уникальности
def add_vacancy_to_db(collection, vacancy_info):
    if not collection.find_one({"_id": vacancy_info["_id"]}):
        collection.insert_one(vacancy_info)

# функция для поиска вакансии с ЗП больше введенной суммы
def search_vacancy_salary(collection, salary):


if __name__ == '__main__':
    vacancy = input("Введите слова для поиска:")
    vacancy_info = get_vacancy_info(vacancy)
    #df = pd.DataFrame.from_records(vacancy_info)
    #df.to_csv("df.csv")
    # подключаемся к БД
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        collection = db["new_social"]
        collection.insert_many(vacancy_info)

