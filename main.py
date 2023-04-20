from flask import Flask, render_template
from data import db_session
from forms.sign_in import LoginForm
from forms.teacher import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/magazine.db")


@app.route('/')
def index():
    return render_template('html/base.html')



@app.route('/select')
def select():
    return render_template('html/select_user_type.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     user = db_sess.query(User).filter(User.email == form.email.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         return redirect("/")
    #     return render_template('login.html',
    #                            message="Неправильный логин или пароль",
    #                            form=form)
    return render_template('html/sign_in.html', title='Авторизация', form=form)


@app.route('/sign_up_as_teacher')
def sign_up():
    form = RegisterForm()
    # if form.validate_on_submit():
    #     if form.password.data != form.password_again.data:
    #         return render_template('register.html', title='Регистрация',
    #                                form=form,
    #                                message="Пароли не совпадают")
    #     db_sess = db_session.create_session()
    #     if db_sess.query(User).filter(User.email == form.email.data).first():
    #         return render_template('register.html', title='Регистрация',
    #                                form=form,
    #                                message="Такой пользователь уже есть")
    #     user = User(
    #         name=form.name.data,
    #         email=form.email.data,
    #         about=form.about.data
    #     )
    #     user.set_password(form.password.data)
    #     db_sess.add(user)
    #     db_sess.commit()
    #     return redirect('/login')
    return render_template('html/sign_up.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
