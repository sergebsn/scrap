import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
  }


u_name = str(input("Input username: "))
url = f"https://api.github.com/user/{u_name}/repos"
request1 = requests.get(url, headers=headers)

json_data = json.loads(request1.text)

for i in json_data:
    len_js = len(json_data)
    dict_j = dict(i) 
    print(dict_j.get('full_name'))


