from flask import request, flash, render_template, redirect, url_for
# from db import get_db
import spider
import pymysql
from flask import Flask
# from pymysql.constants import CLIENT

# import os
# from flask_script import Shell

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='_5#y2L"F4Q8z\n\xec]/',
)


# 初始界面:开始爬虫、进入索引界面
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['start']:
            spider.get_number()
            messages = spider.get_msg()
            flash('爬取完成')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='liaocfe',
                port=3306,
                db='bingyanProject0'
            )
            cursor = db.cursor()
            for message in messages:
                sql = "INSERT INTO documents(title,number,author,time,subject,url_pdf) VALUES" + str(message) + ";"
                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    flash('数据写入失败!', e)
                    db.rollback()
                flash('完成')
        if request.form['Initialized the database']:
            try:
                init_db()
            except Exception:
                flash('初始化失败')
            else:
                flash('数据库已初始化')
    return render_template('index.html')


# 索引
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
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
            db='bingyanProject0'
        )
        cursor = db.cursor()
        sql = ''
        if key:
            sql = "SELECT * FROM documents WHERE CONCAT(title,number,author,time) LIKE '%" + str(key) + "%';"
        if key_words:
            sql = "SELECT * FROM documents WHERE title LIKE '%" + str(key_words) + "%';"
        if key_numbers:
            sql = "SELECT * FROM documents WHERE number LIKE '%" + str(key_numbers) + "%';"
        if key_time:
            sql = "SELECT * FROM documents WHERE time LIKE '%" + str(key_time) + "%';"
        if key_author:
            sql = "SELECT * FROM documents WHERE author LIKE '%" + str(key_author) + "%';"
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
        sql1 ='DROP TABLE IF EXISTS documents;'
        sql2 = """CREATE TABLE documents(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL ,
            number VARCHAR(255) NOT NULL ,
            author VARCHAR(255) NOT NULL ,
            time VARCHAR(255) NOT NULL ,
            subject VARCHAR(255) NOT NULL ,
            url_pdf VARCHAR(255)
        );"""
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.close()
    except Exception:
        print('初始化失败！')
    else:
        print('数据库已初始化！')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
