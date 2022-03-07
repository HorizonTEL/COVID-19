import flask
from flask import Flask
from COVID.settings import *
# from COVID.models.model import db 在user文件中已经给出
from COVID.models.country import *
from COVID.models.province import *
from COVID.models.user import *
from COVID.models.day import *
from COVID.models.news import *
from COVID.utils import *
from flask import request

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
            )
app.config.from_object(MySQLConfig)


# @app.before_first_request
def create_db():
    db.drop_all()  # 每次运行，先删除再创建
    db.create_all()
    # 初始化user
    initial_user()
    initial_day()
    all_map()
    all_country_data()
    all_province_data()
    get_day_data()
    get_top5_data()
    get_news()


with app.app_context():
    db.init_app(app)
    create_db()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        '''
        此处得添加一些防火墙
        '''
        if valid_login(account, password):
            change_time(account, True)
            response = flask.redirect('index')
            response.set_cookie('account', account)
            response.set_cookie('password', hash_password(account))
            return response
        else:
            return flask.render_template('login.html', wrong='用户名或密码错误')
    elif request.method == 'GET':
        return flask.render_template('login.html')


@app.route('/logout')
def logout():
    account = request.cookies.get('account')
    # print(account)
    change_time(account, False)
    response = flask.redirect('index')
    response.delete_cookie("account")
    response.delete_cookie("password")
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        phone_number = request.form.get('Phone')
        if account_exist(account):
            return flask.render_template('register.html', wrong="用户名已存在")
        user = User(account=account, password=password, phone_number=phone_number, CreateTime=getNowDataTime())
        db.session.add(user)
        db.session.commit()
        return flask.redirect('login')
    elif request.method == 'GET':
        return flask.render_template('register.html')


@app.route('/index')
def index():
    account = request.cookies.get('account')
    # print(account)
    password = request.cookies.get('password')
    # print(password)
    if account != None and password != None:
        return flask.render_template('index.html', account=account)
    else:
        return flask.render_template('index.html')


@app.route('/main')
def main_():
    account = request.cookies.get('account')
    password = request.cookies.get('password')
    data = web_number()
    if account != None and password != None:
        return flask.render_template('main.html', confirmed=data[0], died=data[1], cured=data[2], curConfirm=data[3], data=read_news())
    else:
        return flask.redirect('index')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        co = request.args.get('co')
        co_name = Country.query.filter(Country.country_name.contains(co)).all()
        c_name = "提示(国家或地区):"
        if len(co_name) == 0:
            c_name += "无此国家或地区"
        else:
            for i in range(len(co_name)):
                if i == 0:
                    c_name = c_name + co_name[i].country_name
                else:
                    c_name = c_name + "," + co_name[i].country_name
        resp = flask.make_response(c_name)
        return resp
    if request.method == "POST":
        co = request.form.get('co')
        if co == "":
            result = ""
        else:
            co_name = Country.query.filter(Country.country_name == co).first()
            result = []
            if co_name:
                result = [co_name.country_name, co_name.country_curConfirm, co_name.country_confirmed, co_name.country_cured, co_name.country_died]
                # print(result)
        data = web_number()
        return flask.render_template('main.html', confirmed=data[0], died=data[1], cured=data[2], curConfirm=data[3],
                                     data=read_news(), result=result)


@app.route('/get_day_data')
def data_day():
    get_day_data()

if __name__ == "__main__":
    app.run()
