from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class SaveMark(FlaskForm):
    id_student = StringField()
    mark = StringField()
    date = StringField()
    submit = SubmitField('Сохранить')
