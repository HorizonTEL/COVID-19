from selenium import webdriver
from selenium.webdriver.common.by import By
# from time import sleep
from COVID.models.model import *


class News(db.Model):
    __tablename__ = "news"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_href = db.Column(db.String(128))
    news_name = db.Column(db.String(256))


def get_news():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:/application/Google/Chrome/Application/chrome.exe"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument("headless")
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    bro = webdriver.Chrome("C:/code/python/COVID/static/chromedriver.exe", options=options)
    bro.get('https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner')

    news = bro.find_elements(By.XPATH, '//div[@id="ptab-1"]/div[3]/div')
    data = []
    for i in range(5):
        news_href = news[i].find_element(By.XPATH, './div[2]/a').get_attribute('href')
        news_name = news[i].find_element(By.XPATH, './div[2]//div').text
        data.append(News(news_href=news_href, news_name=news_name))

    bro.quit()
    db.session.query(News).delete(synchronize_session=False)
    db.session.add_all(data)
    db.session.commit()


def read_news():
    news = News.query.limit(5)
    data = []
    for i in range(5):
        data.append({'href': news[i].news_href, 'name': news[i].news_name})
    return data
