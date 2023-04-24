from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.schools import School

class EditForm(FlaskForm):
    db_session.global_init("db/magazine.db")
    db_sess = db_session.create_session()
    email = StringField('Логин', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    surname = StringField('Отчество', validators=[DataRequired()])
    # school = SelectField('Школа', choices=[f'{sch.id} - {sch.title}' for sch in db_sess.query(School).all()], validators=[DataRequired()])
    school = SelectField('Школа', choices=['Школа 1', 'Школа 2'], validators=[DataRequired()])
    submit = SubmitField('Сохранить')