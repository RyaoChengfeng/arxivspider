from flask import request, g, flash, Blueprint, render_template, redirect
# from db import get_db
import spider
import pymysql

bp = Blueprint('bp', __name__)


# 初始界面
@bp.route('/', method=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['start']:
            spider.get_number()
            messages = spider.get_msg()
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
                flash("正在写入数据 ")
                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    flash('数据写入失败!', e)
                    db.rollback()
                flash('完成')

        elif request.form['key_words']:
            # 索引
            key_word = request.form['key_words']
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='liaocfe',
                port=3306,
                db='bingyanProject0'
            )
            cursor = db.cursor()
            sql = "SELECT title FROM documents WHERE title LIKE ?", (key_word,)
            results = cursor.execute(sql).fetchall()
            if not results[0]:
                flash('没有找到对应的论文！')

        render_template('index.html')

if __name__ =='__main__':
    bp=Flask