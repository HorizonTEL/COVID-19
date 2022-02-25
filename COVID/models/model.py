from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By

# 实例化一个数据库
db = SQLAlchemy()


def all_map():
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.binary_location = r"C:\application\Google\Chrome\Application\chrome.exe"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    bro = webdriver.Chrome("C:/code/python/COVID/static/chromedriver.exe", options=options)
    bro.get('https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner')
    bro.maximize_window()

    pic = bro.find_element(By.XPATH, '//div[@class="VirusMap_1-1-323_2Urx2E"]')
    pic.screenshot('C:/code/python/COVID/static/image')
    # pic.screenshot('./map.png')

    # sleep(2)
    bro.quit()
