
import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

def get_weather(city, appid):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'
    return requests.get(url)

path = "cred.txt"
with open(path, "r") as f:
    #tmp = f.readlines()
#print(tmp)

    USERNAME, PASSWORD, KEY = f.readlines()
    USERNAME = USERNAME.strip()
    PASSWORD = PASSWORD.strip()
    print(USERNAME, PASSWORD, KEY)


city = input('Enter the city name:')
r = get_weather(city, KEY)
pprint(dict(r.json()))
