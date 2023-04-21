from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.regions import Region
from data.schools import School

class RegisterForm(FlaskForm):
    db_session.global_init("db/magazine.db")
    db_sess = db_session.create_session()
    email = StringField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    surname = StringField('Отчество', validators=[DataRequired()])
    region = SelectField('Регион', choices=[f'{reg.id} - {reg.title}' for reg in db_sess.query(Region).all()])
    school = SelectField('Школа', choices=[], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')