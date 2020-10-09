from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class IndexForm(FlaskForm):
    start = SubmitField('Start Spider')
    init_db = SubmitField('初始化数据库')
    hour = IntegerField('小时:')
    minute = IntegerField('分钟:')
    sched_start = SubmitField('开始执行自动爬取')
    stop_start = SubmitField('停止自动爬取')


class DownloadForm(FlaskForm):
    download = SubmitField('下载')
    number = StringField('请输入论文序号：arXiv:', validators=[DataRequired(message='请输入论文序号！')])



