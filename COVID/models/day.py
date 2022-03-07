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

    
def initial_day():
    days = [
        Day(day_time='', day_confirm=3757, day_died=12, day_cured=312),
        Day(day_time='', day_confirm=6816, day_died=36, day_cured=345),
        Day(day_time='', day_confirm=6707, day_died=89, day_cured=327),
        Day(day_time='', day_confirm=2818, day_died=40, day_cured=325),
        Day(day_time='', day_confirm=4227, day_died=73, day_cured=362),
        Day(day_time='', day_confirm=5347, day_died=80, day_cured=376),
        Day(day_time='', day_confirm=5386, day_died=254, day_cured=597),
        Day(day_time='', day_confirm=14376, day_died=326, day_cured=624),
        Day(day_time='', day_confirm=38612, day_died=424, day_cured=667),
        Day(day_time='', day_confirm=40351, day_died=376, day_cured=710),
        Day(day_time='', day_confirm=20092, day_died=198, day_cured=648),
        Day(day_time='', day_confirm=49768, day_died=408, day_cured=614),
        Day(day_time='', day_confirm=23642, day_died=341, day_cured=712),
        Day(day_time='', day_confirm=19272, day_died=233, day_cured=806),
        Day(day_time='', day_confirm=25072, day_died=513, day_cured=806)
    ]
    
    db.session.add_all(days)
    db.session.commit()


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
