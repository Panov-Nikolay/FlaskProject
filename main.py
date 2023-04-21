from flask import Flask, render_template, redirect
from data import db_session
from forms.sign_in import LoginForm
from forms.sing_up import RegisterForm
from data.students import Student
from data.teachers import Teacher
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/magazine.db")
# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('html/base.html')



@app.route('/select')
def select():
    return render_template('html/select_user_type.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = ([db_sess.query(Student).filter(Student.login == form.email.data).first()] +
                [db_sess.query(Teacher).filter(Teacher.login == form.email.data).first()])
        if user[0] and user[0].check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('html/sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('html/sign_in.html', title='Авторизация', form=form)


@app.route('/sign_up_as_teacher', methods=['GET', 'POST'])
def sign_up_as_teacher():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('html/sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Teacher).filter(Teacher.login == form.email.data).first():
            return render_template('html/sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Teacher(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            surname=form.surname.data,
            id_school=form.school.data,
            login=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('html/sign_up.html', title='Регистрация', form=form)



if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
