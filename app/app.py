# 功能：
# 开始爬虫
# 初始化数据库
# 全局搜索，按标题、序号、作者、时间搜索数据库并返回相关的信息
# 开始定时爬取、关闭定时爬取


from flask import request, flash, render_template, redirect
import pymysql
from flask import Flask
import time
import datetime
from forms import IndexForm, DownloadForm
from spiders import muti_spider

# from pymysql.constants import CLIENT
# from db import get_db
# import os
# from flask_script import Shell

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='_5#y2L"F4Q8z\n\xec]/',
)


# 初始界面:开始爬虫、进入索引界面
@app.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if request.method == 'POST':
        # 整个是用来判断执行哪一个语句

        if form.start.data:  # 表单
            try:
                muti_spider.msg()
            except Exception as e:
                flash('大概是ip被禁了~~')
                print(e)

        if form.stop_start.data:
            sched_start(stop=True)
            flash('已停止自动爬取')

        # 定时
        if form.sched_start.data:  # 表单  # 判断格式合理
            hour = form.hour.data
            minute = form.minute.data
            print(hour, minute)
            form.hour.data = ''
            form.minute.data = ''
            if hour and minute:
                hour = int(hour)
                minute = int(minute)
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    print('时间设置成功')
                    print('定时开始')
                    print('每天 %s 时 %s 分将开始爬取数据' % (hour, minute))
                    sched_start(h=hour, m=minute)
                else:
                    flash('请输入正确的时间格式！')
            else:
                print('自动爬取开始')
                sched_start()

        if form.init_db.data:  # 表单
            try:
                init_db()
            except Exception as e:
                flash('初始化失败')
                print(e)
            else:
                flash('数据库已初始化')

    return render_template('index.html', form=form)


# 索引和下载
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        # 判断类型
        key = request.form['key']
        key_words = request.form['key_words']
        key_numbers = request.form['key_numbers']
        key_time = request.form['key_time']
        key_author = request.form['key_author']
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='liaocfe',
            port=3306,
            db='bingyanProject0',
        )
        cursor = db.cursor()
        sql = ''
        if key:
            sql = "SELECT title,number,author,subject,url_pdf FROM documents WHERE CONCAT(title,number,author,time) LIKE '%" + str(
                key) + "%';"
        if key_words:
            sql = "SELECT title,number,author,subject,url_pdf FROM documents WHERE title LIKE '%" + str(
                key_words.lower().title()) + "%';"
        if key_numbers:
            sql = "SELECT title,number,author,subject,url_pdf FROM documents WHERE number LIKE '%" + str(
                key_numbers) + "%';"
        if key_time:
            sql = "SELECT title,number,author,subject,url_pdf FROM documents WHERE time LIKE '%" + str(
                key_time) + "%';"
        if key_author:
            sql = "SELECT title,number,author,subject,url_pdf FROM documents WHERE author LIKE '%" + str(
                key_author) + "%';"
        if sql:
            cursor.execute(sql)
            results = cursor.fetchall()
            results = list(results)
            if not results:
                flash('没有找到对应的论文！')
        else:
            flash('请输入关键字！')
        db.close()
    return render_template('search.html', results=results)


# 下载接口
@app.route('/download', methods=['GET', 'POST'])
def download():
    form = DownloadForm()
    if request.method == 'POST':
        number = form.number.data
        print(number)
        form.number.data = ''
        flash('为您提供下载论文 arXiv: %s的链接' % number)
        return redirect('http://81.68.250.220/download/' + number + '.pdf')
    return render_template('download.html', form=form)


#  初始化数据库
def init_db():
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='liaocfe',
        port=3306,
        db='bingyanProject0',
    )
    cursor = db.cursor()
    try:
        sql1 = 'DROP TABLE IF EXISTS documents;'
        # 有的论文标题太长、有的作者太多
        sql2 = """CREATE TABLE documents(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(500) NOT NULL ,
            number VARCHAR(255) NOT NULL ,
            author VARCHAR(1000) NOT NULL , 
            time VARCHAR(255) NOT NULL ,
            subject VARCHAR(255) NOT NULL ,
            url_pdf VARCHAR(255)
        );"""
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.close()
    except Exception as e:
        print('初始化失败！')
        print(e)
    else:
        print('数据库已初始化！')


# 定时爬取,可设置时和分
def sched_start(h=None, m=None, stop=False):
    while True:
        if stop:
            break
        now = datetime.datetime.now()
        if h and m:
            sched_time = datetime.datetime(now.year, now.month, now.day, h, m, now.second)
        else:
            sched_time = datetime.datetime.now() + datetime.timedelta(days=1)

        if time.mktime(now.timetuple()) > time.mktime(sched_time.timetuple()):
            sched_time += datetime.timedelta(days=1)
            muti_spider.msg()  # 执行爬虫

        time.sleep(600)  # 每10分钟检测一次


if __name__ == '__main__':
    app.run(debug=True)
