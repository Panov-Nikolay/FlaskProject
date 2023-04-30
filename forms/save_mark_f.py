from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class SaveMarkF(FlaskForm):
    id_student = StringField()
    mark = StringField()
    part = StringField()
    submit = SubmitField('Сохранить')
