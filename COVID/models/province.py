from selenium import webdriver
from selenium.webdriver.common.by import By
from COVID.models.model import *
import requests
import re


# 各个省份的疫情数据
class Province(db.Model):
    __tablename__ = "province"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    province_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province_name = db.Column(db.String(32))
    province_add = db.Column(db.Integer)
    province_curConfirm = db.Column(db.Integer)
    province_confirmed = db.Column(db.Integer)
    province_cured = db.Column(db.Integer)
    province_died = db.Column(db.Integer)


def all_province_data():
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
    bro.find_element(By.XPATH, '//div[@id="nationTable"]/div').click()

    provinces = bro.find_elements(By.XPATH, '//div[@id="nationTable"]//tbody/tr')
    # print(provinces)
    data = []
    for province in provinces:
        province_name = province.find_element(By.XPATH, './/td//span[2]').text
        try:
            province_add = int(province.find_element(By.XPATH, './/td[2]').text)
        except:
            province_add = 0
        province_curConfirm = int(province.find_element(By.XPATH, './/td[3]').text)
        province_confirmed = int(province.find_element(By.XPATH, './/td[4]').text)
        province_cured = int(province.find_element(By.XPATH, './/td[5]').text)
        province_died = int(province.find_element(By.XPATH, './/td[6]').text)
        data.append(Province(
            province_name=province_name, province_add=province_add, province_curConfirm=province_curConfirm,
            province_confirmed=province_confirmed, province_cured=province_cured, province_died=province_died)
        )

    bro.quit()

    db.session.add_all(data)
    db.session.commit()


def web_number():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/97.0'
    }
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"

    response = requests.get(url=url, headers=headers).text
    ex = '"summaryDataIn":(.*?)},'
    # string
    numbers = re.findall(ex, response, re.S)[0] + '}'
    # print(numbers)
    confirmed = int(re.findall('confirmed":"(.*?)",', numbers, re.S)[0])    # 累计确诊
    died = int(re.findall('died":"(.*?)",', numbers, re.S)[0])              # 累计死亡
    cured = int(re.findall('cured":"(.*?)",', numbers, re.S)[0])            # 累计治愈
    curConfirm = int(re.findall('curConfirm":"(.*?)",', numbers, re.S)[0])  # 现有确诊
    '''
    print(confirmed)
    print(died)
    print(cured)
    print(curConfirm)
    '''
    return [curConfirm, confirmed, cured, died]
