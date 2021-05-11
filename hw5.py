import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
#MONGO_URI = "127.0.0.1:27017"

DRIVER_PATH = "./chromedriver"

driver = webdriver.Chrome(DRIVER_PATH)
url = "https://vk.com/tokyofashion"
driver.get(url)

search_url = driver.find_element_by_class_name('ui_tab_search').get_attribute('href')
driver.get(search_url)
search = driver.find_element_by_id("wall_search")
search.send_keys("прическа" + Keys.ENTER)

scroll = 1
while True:
    time.sleep(2)
    try:
        button = driver.find_element_by_class_name('JoinForm__notNow')
        if button:
            button.click()
    except Exception as e:
        print(e)
    finally:
        driver.find_element_by_tag_name("html").send_keys(Keys.END)
        scroll += 1
        time.sleep(1)
        wall = driver.find_element_by_id('fw_load_more')
        stopscroll = wall.get_attribute('style')
        if stopscroll == 'display: none;':
            break

posts = driver.find_element_by_xpath('//div[@id="page_wall_posts"]//..//img[contains(@alt, "Tokyo Fashion")]/../../..')
#posts = driver.find_element_by_xpath('//div[contains(@id, "post-")]')

pst = 0
post_info = []
for post in posts:
    post_data = {}
    post_day = post.find_element_by_class_name('rel_date').text
    post_text = post.find_element_by_class_name('wall_post_text').text
    post_link = post.find_element_by_class_name('post_link').get_attribute('href')
    post_photo_links_list = []
    post_photo_links = post.find_elements_by_xpath('.//a[contains(@aria-label,"Original")]')
    for photo in post_photo_links:
        photo_link = photo.get_attribute('area-label').split()[2]
        post_photo_links_list.append(photo_link)
    post_likes = int(post.find_element_by_class_name('like_button_count')[0].text)
    post_share = int(post.find_element_by_class_name('like_button_count')[1].text)

    post_data['post_day'] = post_day
    post_data['post_text'] = post_text
    post_data['post_link'] = post_link
    post_data['post_photo_links_list'] = post_photo_links_list
    post_data['post_likes'] = post_likes
    post_data['post_share'] = post_share

    posts_info.append(post_data)
    pst += 1
    print(pst)

db = client['tokyo_post']
collection = db.collection
collection.insert_many(post_info)