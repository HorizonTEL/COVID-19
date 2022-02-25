# mysql settings
class MySQLConfig(object):
    DEBUGE = True
    SECRET_KEY = "root"
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/covid"
    SQLALCHEMY_TRACK_MODIFICATIONS = True   # 动态追踪修改设置
    SQLALCHEMY_ECHO = True
