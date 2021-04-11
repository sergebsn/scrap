
import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


def get_weather(city, appid):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'
    return requests.get(url)


key = os.getenv('cred.txt') # я не понимаю что не так, на сайте openweathermap зарегился, создал ключ апи, сделал env,
# положил в файл свой логин и пароль и ключ АПИ
city = input('Enter the city name:')
r = get_weather(city, key)
pprint(dict(r.json()))
