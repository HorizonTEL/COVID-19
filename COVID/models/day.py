import requests
import re
from COVID.models.model import *
import matplotlib.pyplot as plt
from datetime import datetime


class Day(db.Model):
    __tablename__ = "day"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    day_time = db.Column(db.String(32), primary_key=True)
    day_confirm = db.Column(db.Integer)
    day_cured = db.Column(db.Integer)
    day_died = db.Column(db.Integer)


def get_day_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/97.0'
    }
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"

    response = requests.get(url=url, headers=headers).text

    ex = '"summaryDataIn":(.*?)},'
    # string
    numbers = re.findall(ex, response, re.S)[0] + '}'
    # print(numbers)
    day_time = str(datetime.now().month) + '.' + str(datetime.now().day)
    day_confirm = int(re.findall('confirmedRelative":"(.*?)",', numbers, re.S)[0])  # 新增确诊
    day_cured = int(re.findall('diedRelative":"(.*?)",', numbers, re.S)[0])  # 新增死亡
    day_died = int(re.findall('curedRelative":"(.*?)",', numbers, re.S)[0])  # 新增治愈
    '''
    print(confirmedRelative)
    print(diedRelative)
    print(curedRelative)
    '''
    if_day_exist = Day.query.filter(Day.day_time == day_time).first()
    if if_day_exist:
        print("今日数据已经存入，请勿重复存入")
        return
    day = Day(day_time=day_time, day_confirm=day_confirm,
              day_died=day_died, day_cured=day_cured)
    if Day.query.count() >= 91:
        # 多余数据删除
        db.session.query(Day).limit(Day.query.count() - 90).delete(synchronize_session=False)
        db.session.commit()
    db.session.add(day)
    db.session.commit()
