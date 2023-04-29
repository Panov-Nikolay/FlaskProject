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
from data.subject_plan import SubjectPlan
from data.final_marks import FinalMarks
from data.marks import Marks
from datetime import datetime


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
                if user.__class__.__name__ == 'Student':
                    return redirect("/student_start")
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
    school = db_sess.query(School).filter(School.id == current_user.id_school).first()
    classes = []
    for i in db_sess.query(TeacherClass).filter(TeacherClass.id_teacher == current_user.id).all():
        classes.append((db_sess.query(Class).filter(Class.id == i.id_class).first(), db_sess.query(Subjects).filter(Subjects.id == i.id_subject).first()))
    return render_template('html/teachers_school.html',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
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
        user.id_school=form.school.data
        user.login=form.email.data
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


@app.route('/teachers_school/<int:id_class>/<int:id_subject>', methods=['GET', 'POST'])
def get_students(id_class, id_subject):
    db_sess = db_session.create_session()
    form = (db_sess.query(Class).filter(Class.id == id_class).first(), db_sess.query(Subjects).filter(Subjects.id == id_subject).first())
    students = db_sess.query(Student).filter(Student.id_class == id_class).all()
    return render_template('html/students.html', user=f'{current_user.first_name[0]}. {current_user.surname[0]}. {current_user.last_name}',
                           logo=form, students=students)


@app.route('/student_start', methods=['GET'])
def student_start():
    db_sess = db_session.create_session()
    class_id = db_sess.query(Student).filter(Student.id == current_user.id).first().id_class
    class1 = db_sess.query(Class).filter(Class.id == class_id).first()
    school_id = class1.id_school
    school = db_sess.query(School).filter(School.id == school_id).first()
    return render_template('html/student_start.html',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=[school.title, class1.title])


@app.route('/student_marks/<int:id_class>/<int:id_student>', methods=['GET'])
def student_marks(id_class, id_student):
    db_sess = db_session.create_session()


@app.route('/timetable/<logo>', methods=['GET'])
def timetable(logo):
    db_sess = db_session.create_session()
    lessons = db_sess.query(SubjectPlan).filter(SubjectPlan.id_class == current_user.id_class).all()
    timetable = [{} for _ in range(6)]
    logo = logo[2:-2].split(',')
    logo = logo[0][:-1] + ', ' + logo[1][2:]
    for i in lessons:
        timetable[i.day - 1][i.lesson] = db_sess.query(Subjects).filter(i.id_subject == Subjects.id).first().title
    return render_template('html/timetable.html',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=logo, table=timetable)


@app.route('/final_marks_student/<logo>', methods=['GET'])
def final_marks(logo):
    db_sess = db_session.create_session()
    part0 = db_sess.query(FinalMarks).filter(FinalMarks.id_student == current_user.id).all()
    part1, part2, part3, part4, part_f = [], [], [], [], []
    for i in part0:
        print(i, i.part)
        if i.part == 1:
            part1.append(i)
        elif i.part == 2:
            part2.append(i)
        elif i.part == 3:
            part3.append(i)
        elif i.part == 4:
            part4.append(i)
        elif i.part == 5:
            part_f.append(i)
    s1, s2, s3, s4, s5 = [], [], [], [], []
    for i in range(len(part1)):
        s1.append([db_sess.query(Subjects).filter(Subjects.id == part1[i].id_subject).first().title, part1[i].mark])
        s2.append([db_sess.query(Subjects).filter(Subjects.id == part2[i].id_subject).first().title, part2[i].mark])
        s3.append([db_sess.query(Subjects).filter(Subjects.id == part3[i].id_subject).first().title, part3[i].mark])
        s4.append([db_sess.query(Subjects).filter(Subjects.id == part4[i].id_subject).first().title, part4[i].mark])
        s5.append([db_sess.query(Subjects).filter(Subjects.id == part_f[i].id_subject).first().title, part_f[i].mark])
    s1.sort(key=lambda x: x[0])
    s2.sort(key=lambda x: x[0])
    s3.sort(key=lambda x: x[0])
    s4.sort(key=lambda x: x[0])
    s5.sort(key=lambda x: x[0])
    logo = logo[2:-2].split(',')
    logo = logo[0][:-1] + ', ' + logo[1][2:]
    return render_template('html/final_marks.html',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=logo, marks=[s1, s2, s3, s4, s5])


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')



