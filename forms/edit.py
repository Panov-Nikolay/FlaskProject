from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.schools import School
from data.classes import Class


class EditForm(FlaskForm):
    db_session.global_init("db/magazine.db")
    db_sess = db_session.create_session()
    email = StringField('Логин', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    last_name = StringField('Отчество', validators=[DataRequired()])
    school = SelectField('Школа', choices=[sch.title for sch in db_sess.query(School).all()],
                         validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EditFormS(FlaskForm):
    db_session.global_init("db/magazine.db")
    db_sess = db_session.create_session()
    email = StringField('Логин', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    last_name = StringField('Отчество', validators=[DataRequired()])
    school = SelectField('Школа', choices=[sch.title for sch in db_sess.query(School).all()],
                         validators=[DataRequired()])
    class1 = StringField('Класс', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
