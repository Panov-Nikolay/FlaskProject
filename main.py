from flask import Flask, render_template, redirect
from data import db_session
from forms.sign_in import LoginForm
from forms.sing_up import RegisterForm
from data.students import Student
from data.teachers import Teacher
from data.schools import School
from forms.edit import EditForm
from data.classes import Class
from data.teacher_class import TeacherClass
from data.subjects import Subjects
from data.marks import Marks


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
                [db_sess.query(Teacher).filter(Teacher.login == form.email.data).first()]))
        if len(user) != 0:
            user = user[0]
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
    db_sess = db_session.create_session()
    classes = []
    school = db_sess.query(School).filter(School.id == current_user.id_school).first()
    for i in db_sess.query(TeacherClass).filter(TeacherClass.id_teacher == current_user.id).all():
        classes.append((db_sess.query(Class).filter(Class.id == i.id_class).first(), db_sess.query(Subjects).filter(Subjects.id == i.id_subject).first()))
    return render_template('html/teachers_school.html',
                           user=f'{current_user.first_name[0]}. {current_user.surname[0]}. {current_user.last_name}',
                           logo=school, classes=classes)


@app.route('/teacher_profile', methods=['GET', 'POST'])
def teacher_profile():
    global current_user
    form = EditForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Teacher).filter(Teacher.id == current_user.id).first()
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        user.surname=form.surname.data
        user.id_school=int(form.school.data[0])
        user.login=form.email.data
        current_user.first_name=form.first_name.data
        current_user.last_name=form.last_name.data
        current_user.surname=form.surname.data
        current_user.id_school= int(form.school.data[0])
        current_user.login=form.email.data
        db_sess.commit()
        return redirect('/teachers_school')
    return render_template('html/teacher_profile.html', form=form, user=current_user)

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect('/')


@app.route('/teachers_school/<int:id_class>/<int:id_subject>', methods=['GET', 'POST'])
def get_students(id_class, id_subject):
    db_sess = db_session.create_session()
    form = (db_sess.query(Class).filter(Class.id == id_class).first(), db_sess.query(Subjects).filter(Subjects.id == id_subject).first())
    students = sorted(db_sess.query(Student).filter(Student.id_class == id_class).all(), key=lambda x: x.surname)
    marks = {}
    for student in students:
        # marks[student.id] = db_sess.query(Marks).filter(Marks.id_student == student.id, Marks.id_subject == id_subject).all()
        marks[student.id] = '0' * 50
    return render_template('html/students.html', user=f'{current_user.first_name[0]}. {current_user.surname[0]}. {current_user.last_name}',
                           logo=form, students=students, marks=marks)

if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
