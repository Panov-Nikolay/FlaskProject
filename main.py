from flask import Flask, render_template, redirect
from data import db_session
from forms.sign_in import LoginForm
from forms.sing_up import RegisterForm
from data.students import Student
from data.teachers import Teacher
from data.schools import School
from forms.edit import EditForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/magazine.db")


@app.route('/')
def index():
    return render_template('html/start_page.html')


@app.route('/select')
def select():
    return render_template('html/select_user_type.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    global current_user
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = list(filter(lambda x: x != None, [db_sess.query(Student).filter(Student.login == form.email.data).first()] +
                [db_sess.query(Teacher).filter(Teacher.login == form.email.data).first()]))[0]
        if user and user.check_password(form.password.data):
            current_user = user
            if user.__class__.__name__ == 'Teacher':
                return redirect("/teachers_school")
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

@app.route('/teachers_school', methods=['GET', 'POST'])
def schools():
    return render_template('html/teachers_school.html',
                           user=f'{current_user.first_name[0]}. {current_user.surname[0]}. {current_user.last_name}',
                           logo=current_user.id_school, classes=['1A', '2A', '3A', '4A', '5A'])


@app.route('/teacher_profile', methods=['GET', 'POST'])
def teacher_profile():
    global current_user
    form = EditForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        current_user.first_name=form.first_name.data
        current_user.last_name=form.last_name.data
        current_user.surname=form.surname.data
        current_user.id_school=form.school.data
        current_user.login=form.email.data
        db_sess.commit()
        return redirect('/teachers_school')
    return render_template('html/teacher_profile.html', form=form, user=current_user)

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
