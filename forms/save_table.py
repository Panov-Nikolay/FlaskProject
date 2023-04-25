from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class SaveTable(FlaskForm):
    submit = SubmitField('Сохранить')