from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from COVID.models.model import *
import matplotlib.pyplot as plt


# 各个国家的疫情数据
class Country(db.Model):
    __tablename__ = "country"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column(db.String(32))
    country_curConfirm = db.Column(db.Integer)
    country_confirmed = db.Column(db.Integer)
    country_cured = db.Column(db.Integer)
    country_died = db.Column(db.Integer)


def all_country_data():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:/application/Google/Chrome/Application/chrome.exe"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument("headless")
    prefs = {
        'profile.default_content_setting_values': {'images': 2}
    }
    options.add_experimental_option('prefs', prefs)
    bro = webdriver.Chrome("C:/code/python/COVID/static/chromedriver.exe", options=options)
    bro.get('https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner')
    bro.find_element(By.XPATH, '//div[@id="foreignTable"]/div').click()

    countrys = bro.find_elements(By.XPATH, '//div[@id="foreignTable"]//tbody//table//tr')
    # print(countrys)
    data = []
    for country in countrys:
        try:
            country_name = country.find_element(By.XPATH, './/a/div').text
        except:
            country_name = country.find_element(By.XPATH, './/div').text

        country_curConfirm = int(country.find_element(By.XPATH, './/td[2]').text)
        country_confirmed = int(country.find_element(By.XPATH, './/td[3]').text)
        country_cured = int(country.find_element(By.XPATH, './/td[4]').text)
        country_died = int(country.find_element(By.XPATH, './/td[5]').text)
        data.append(Country(
            country_curConfirm=country_curConfirm, country_name=country_name,
            country_confirmed=country_confirmed, country_cured=country_cured, country_died=country_died)
        )

    bro.quit()

    db.session.add_all(data)
    db.session.commit()


def get_top5_data():
    countrys = Country.query.order_by(Country.country_curConfirm.desc()).limit(5)
    country_name = []
    country_curConfirm = []
    for country in countrys:
        country_name.append(country.country_name)
        country_curConfirm.append(country.country_curConfirm)

    plt.rcParams['font.family'] = ['Fangsong']
    plt.bar(country_name, country_curConfirm, width=0.5)
    plt.title('全球现存新冠病例TOP5')
    plt.grid(axis='y', linestyle=':')
    # plt.show()
    plt.savefig(r'./static/image/country.png', dpi=500, bbox_inches='tight', transparent=True)
