from COVID.models.model import *
from werkzeug.security import generate_password_hash, check_password_hash  # 转换密码用到的库
from COVID.utils import *


# 用户
class User(db.Model):
    # 数据库的表
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    # 列名
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)   # 用户id
    account = db.Column(db.String(11), unique=True)     # 账号
    password_hash = db.Column(db.String(255))           # 密码
    phone_number = db.Column(db.String(11))             # 手机号
    if_admin = db.Column(db.Boolean, default=False)     # 是否为管理员
    CreateTime = db.Column(db.DateTime)                 # 创建的时间
    LoginTime = db.Column(db.DateTime)                  # 上一次登陆时间
    LogoutTime = db.Column(db.DateTime)                 # 上一次退出时间

    @property
    def password(self):
        raise AttributeError("password isn't visible")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def inial_user():
    # 初始化admin
    admin = User(
        account='admin', password='admin888', if_admin=True, phone_number="12345678901", CreateTime=getNowDataTime()
    )
    db.session.add(admin)

    # 初始化user
    users = [
        User(account='小红', password='123456', phone_number="13852310234", CreateTime=getNowDataTime()),
        User(account='ljh', password='admin888', phone_number="13639065655", CreateTime=getNowDataTime()),
        User(account='wjx', password='wjx', phone_number="13632446567", CreateTime=getNowDataTime()),
        User(account='test', password='test', phone_number="19313426657", CreateTime=getNowDataTime())
    ]
    db.session.add_all(users)

    db.session.commit()


def valid_login(account, password):
    user = User.query.filter(User.account == account, User.if_admin == False).first()
    if user:
        if user.check_password(password):
            return True
    return False


def hash_password(account):
    user = User.query.filter(User.account == account, User.if_admin == False).first()
    if user:
        return user.password_hash
    else:
        return False


def change_time(account, login):
    user = User.query.filter(User.account == account, User.if_admin == False).first()
    if login:
        user.LoginTime = getNowDataTime()
    else:
        user.LogoutTime = getNowDataTime()
    db.session.commit()


def account_exist(account):
    user = User.query.filter(User.account == account, User.if_admin == False).first()
    if user:
        return True
    return False
