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
        Day(day_time='2.21', day_confirm=3757, day_died=12, day_cured=312),
        Day(day_time='2.22', day_confirm=6816, day_died=36, day_cured=345),
        Day(day_time='2.23', day_confirm=6707, day_died=89, day_cured=327),
        Day(day_time='2.24', day_confirm=2818, day_died=40, day_cured=325),
        Day(day_time='2.25', day_confirm=4227, day_died=73, day_cured=362),
        Day(day_time='2.26', day_confirm=5347, day_died=80, day_cured=376),
        Day(day_time='2.27', day_confirm=5386, day_died=254, day_cured=597),
        Day(day_time='2.28', day_confirm=14376, day_died=326, day_cured=624),
        Day(day_time='3.1', day_confirm=38612, day_died=424, day_cured=667),
        Day(day_time='3.2', day_confirm=40351, day_died=376, day_cured=710),
        Day(day_time='3.3', day_confirm=20092, day_died=198, day_cured=648),
        Day(day_time='3.4', day_confirm=49768, day_died=408, day_cured=614),
        Day(day_time='3.5', day_confirm=23642, day_died=341, day_cured=712),
        Day(day_time='3.6', day_confirm=19272, day_died=233, day_cured=806),
        Day(day_time='3.7', day_confirm=25072, day_died=513, day_cured=806),
        Day(day_time='3.8', day_confirm=6166, day_died=280, day_cured=498),
        Day(day_time='3.9', day_confirm=7599, day_died=320, day_cured=640),
        Day(day_time='3.10', day_confirm=11042, day_died=420, day_cured=840),
        Day(day_time='3.11', day_confirm=9585, day_died=579, day_cured=1020),
        Day(day_time='3.12', day_confirm=5824, day_died=285, day_cured=1028),
        Day(day_time='3.13', day_confirm=3234, day_died=326, day_cured=1129),
        Day(day_time='3.14', day_confirm=4102, day_died=392, day_cured=1023),
        Day(day_time='3.15', day_confirm=4001, day_died=343, day_cured=1304),
        Day(day_time='3.16', day_confirm=3543, day_died=254, day_cured=908),
        Day(day_time='3.17', day_confirm=4909, day_died=279, day_cured=1305),
        Day(day_time='3.18', day_confirm=5105, day_died=408, day_cured=1079),
        Day(day_time='3.19', day_confirm=6122, day_died=515, day_cured=1718)
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


def get_all_days():
    Days = Day.query.all()
    confirmed = []
    died = []
    cured = []
    day_time = []
    for day in Days:
        confirmed.append(day.day_confirm)
        died.append(day.day_died)
        cured.append(day.day_cured)
        day_time.append(day.day_time)

    # 每日新增
    plt.rcParams['font.family'] = ['Fangsong']
    plt.plot(day_time, confirmed, label='confirmed')
    plt.xticks(day_time[2::3], rotation=45)
    plt.legend()
    # plt.show()
    plt.title('全国每日新增确诊病例')
    plt.grid(axis='y', linestyle=':')
    plt.savefig(r'./static/image/day1.png', dpi=500, bbox_inches='tight', transparent=True)
    plt.clf()

    # 死亡和治愈
    plt.rcParams['font.family'] = ['Fangsong']
    plt.plot(day_time, died, label='died')
    plt.plot(day_time, cured, label='cured')
    plt.xticks(day_time[2::3], rotation=45)
    plt.legend()
    # plt.show()
    plt.title('全国每日新增治愈和死亡病例')
    plt.grid(axis='y', linestyle=':')
    plt.savefig(r'./static/image/day2.png', dpi=500, bbox_inches='tight', transparent=True)
    plt.clf()
