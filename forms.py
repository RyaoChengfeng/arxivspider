from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class IndexForm(FlaskForm):
    start = SubmitField('Start Spider')
    init_db = SubmitField('初始化数据库')
    hour = IntegerField('小时', validators=[NumberRange(1, 12, '数字超出范围')])
    minute = IntegerField('分钟', validators=[NumberRange(1, 60, '数字超出范围')])
    sched_start = SubmitField('开始执行自动爬取')
    stop_start = SubmitField('停止自动爬取')
