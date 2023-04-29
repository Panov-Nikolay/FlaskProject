from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class SaveMark(FlaskForm):
    id_student = StringField()
    mark = StringField()
    submit = SubmitField('Сохранить')