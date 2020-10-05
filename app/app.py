from flask import request, flash, render_template, redirect, url_for
# from db import get_db
import spider
import pymysql
from flask import Flask

# import os
# from flask_script import Shell

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='_5#y2L"F4Q8z\n\xec]/',
)


# 初始界面
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
                flash("正在写入数据 %s" % message[1])
                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    flash('数据写入失败!', e)
                    db.rollback()
                flash('完成')
    return render_template('index.html')


# 索引(有错误)
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        key_words = request.form['key_words']
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='liaocfe',
            port=3306,
            db='bingyanProject0'
        )
        cursor = db.cursor()
        sql = "SELECT title FROM documents WHERE title LIKE '%" + str(key_words) + "%';"
        cursor.execute(sql)
        results = cursor.fetchone()
        results = list(results)
        if not results[0]:
            flash('没有找到对应的论文！')
            redirect(url_for('index'))
    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
