from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    key_words = StringField('tap in key words', validators=[DataRequired()])
    search = StringField('Search', validators=[DataRequired()])
