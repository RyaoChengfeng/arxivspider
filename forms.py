from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    start = SubmitField('Start Spider')
    init_db = SubmitField('初始化数据库')
    sched_start = SubmitField('开始执行自动爬取')

