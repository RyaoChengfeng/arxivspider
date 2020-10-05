# 目前用不上

import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    db = get_db()
    with current_app.open_resouce("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
        # 执行数据库语句


def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host='localhost',
            user='root',
            password='liaocfe',
            port=3306,
            db='bingyanProject0'
        )
    return g.db


def close_db():
    db = g.pop("db", None)
    if db is not None:
        db.close()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("数据库初始化")


def init_app(app):
    app.teardown_appcontext(close_db)
    # 返回响应后进行清理的时候调用此函数
    app.cli.add_command(init_db_command)
