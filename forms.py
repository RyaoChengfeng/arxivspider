from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class IndexForm(FlaskForm):
    start = SubmitField('Start Spider')
    init_db = SubmitField('初始化数据库')
    hour = IntegerField('小时', validators=[NumberRange(1, 24, '数字范围为1~24！')])
    minute = IntegerField('分钟', validators=[NumberRange(1, 60, '数字范围为1~60！')])
    sched_start = SubmitField('开始执行自动爬取')
    stop_start = SubmitField('停止自动爬取')


class DownloadForm(FlaskForm):
    download = SubmitField('下载')
    number = StringField('请输入论文序号：arXiv:', validators=[DataRequired(message='请输入论文序号！')])



