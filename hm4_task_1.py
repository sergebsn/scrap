# import json
import requests
from lxml import html
from pprint import pprint
# подключаем модуль MongoClient
from pymongo import MongoClient
MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "news"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db["news"]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

def news_lenta():
    url = "https://lenta.ru/"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    xpath_for_item = '//section[@class="row b-top7-for-main js-top-seven"]//div[contains(@class, "item")]' #section[contains(@class, "row b-top7-for-main js-top-seven")]//div[contains(@class, "item")]
    items = dom.xpath(xpath_for_item)
    info_list = []

    for item in items:
        info = {}
        xpath_item_name = ".//a/text()"
        try:
            info["source"] = 'LENTA.RU'
            info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
            info["news_url"] = url+item.xpath(".//a/@href")[0]
            info["news_datetime"] = item.xpath(".//a/time/@datetime")[0]
            info_list.append(info)
        except Exception as e:
            print(e)
    return info_list


            #info["name"] = item.xpath(xpath_item_name)[0]
            #info["img_url"] = item.xpath(".//img/@src")[0]
            #info["price"] = item.xpath('.//span[contains(@class, "__price")]//text()')
            #info_list.append(info)


def news_mail():
    url = "https://news.mail.ru/"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    info_list = []

    xpath_for_item = '//div[@class="wrapper"]//div[@data-module="TrackBlocks"]//div[contains(@class, "__item")]'
    items = dom.xpath(xpath_for_item)
    for item in items:
        info = {}
        xpath_item_name = ".//span[contains(@class, '__title')]/text()"
        try:
            info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
            info["news_url"] = item.xpath(".//a/@href")[0]
            info["source"] = mail_info(item.xpath(".//a/@href")[0])[0]
            info["news_datetime"] = mail_info(item.xpath(".//a/time/@datetime")[0])[1]
            info_list.append(info)
        except Exception as e:
            print(e)

    xpath_for_item = '//ul[contains(@data-module, "TrackBlocks")]//li[@class="list__item"]'
    items = dom.xpath(xpath_for_item)
    for item in items:
        info = {}
        xpath_item_name = ".//a/text()"
        try:
            info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
            info["news_url"] = item.xpath(".//a/@href")[0]
            info["source"] = mail_info(item.xpath(".//a/@href")[0])[0]
            info["news_datetime"] = mail_info(item.xpath(".//a/@href")[0])[1]
            info_list.append(info)
        except Exception as e:
            print(e)
    return info_list

def mail_info(url):
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    xpath_for_item = '//div[@class="breadcrumbs breadcrumbs_article js-ago-wrapper"]'
    items = dom.xpath(xpath_for_item)
    for item in items:
        try:
            source = item.xpath(".//a/span/text()")[0]
            news_datetime = item.xpath('.//span//@datetime')[0]
        except Exception as e:
            print(e)
    return (source, news_datetime)


def insert_to_db(collection, info_list):
    for item in info_list:
        collection.update_one({"$and": [{'news_name':{"$eq": item['news_name']}},{'source': {"$eq": item['source']}}]},
                                    {"$set": item}, upsert=True)
        print("News in BD")




if __name__ == '__main__':
    news = news_lenta()
    pprint(news)
    insert_to_db(collection, news)
    pprint("---------------------------------")
    news = news_mail()
    pprint(news)
    insert_to_db(collection, news)
    pprint("---------------------------------")



