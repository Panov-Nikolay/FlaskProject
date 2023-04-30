from flask import Flask, render_template, redirect
from data import db_session
from forms.sign_in import LoginForm
from forms.sing_up import RegisterForm
from forms.save_mark import SaveMark
from forms.save_mark_f import SaveMarkF
from data.students import Student
from data.teachers import Teacher
from data.schools import School
from forms.edit import EditForm, EditFormS
from data.classes import Class
from data.teacher_class import TeacherClass
from data.subjects import Subjects
from data.subject_plan import SubjectPlan
from data.final_marks import FinalMarks
from data.marks import Marks
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/magazine.db")


def date_division(part):
    if part == 1:
        d1 = datetime.date(year=2022, month=9, day=1)
        d2 = datetime.date(year=2022, month=11, day=1)
    elif part == 2:
        d1 = datetime.date(year=2022, month=11, day=1)
        d2 = datetime.date(year=2023, month=1, day=1)
    elif part == 3:
        d1 = datetime.date(year=2023, month=1, day=1)
        d2 = datetime.date(year=2023, month=4, day=1)
    else:
        d1 = datetime.date(year=2023, month=4, day=1)
        d2 = datetime.date(year=2023, month=6, day=1)
    return [d1, d2]


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
        classes.append((db_sess.query(Class).filter(Class.id == i.id_class).first(),
                        db_sess.query(Subjects).filter(Subjects.id == i.id_subject).first()))
    return render_template('html/teachers_school.html', title='Выбор класса',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=school, classes=classes)


@app.route('/teacher_profile', methods=['GET', 'POST'])
def teacher_profile():
    global current_user
    form = EditForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Teacher).filter(Teacher.id == current_user.id).first()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.surname = form.surname.data
        user.id_school = db_sess.query(School).filter(School.title == form.school.data).first().id
        user.login = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.surname = form.surname.data
        current_user.id_school = db_sess.query(School).filter(School.title == form.school.data).first().id
        current_user.login = form.email.data
        db_sess.commit()
        return redirect('/teachers_school')
    return render_template('html/teacher_profile.html', title='Профиль', form=form, user=current_user)


@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect('/')


@app.route('/teachers_school/<int:id_class>/<int:id_subject>/<int:part>', methods=['GET', 'POST'])
def get_students(id_class, id_subject, part):
    db_sess = db_session.create_session()
    submit_form = SaveMark()
    if submit_form.validate_on_submit():
        db_sess = db_session.create_session()
        mark = db_sess.query(Marks).filter(Marks.id_student == submit_form.id_student.data,
                                           Marks.id_subject == id_subject,
                                           Marks.date == datetime.date(year=int(submit_form.date.data.split('.')[2]),
                                                                       month=int(submit_form.date.data.split('.')[1]),
                                                                       day=int(submit_form.date.data.split('.')[0]))).first()
        if mark is None:
            mark = Marks(
                mark=submit_form.mark.data,
                id_student=int(submit_form.id_student.data),
                id_subject=id_subject,
                date=datetime.date(year=int(submit_form.date.data.split('.')[2]),
                                   month=int(submit_form.date.data.split('.')[1]),
                                   day=int(submit_form.date.data.split('.')[0]))
            )
            print(int(submit_form.date.data.split('.')[2]), int(submit_form.date.data.split('.')[1]),
                                                                int(submit_form.date.data.split('.')[0]))
            db_sess.add(mark)
        else:
            mark.mark = submit_form.mark.data
        db_sess.commit()
        return redirect(f'/teachers_school/{id_class}/{id_subject}/{part}')
    date1, date2 = date_division(part)
    form = (db_sess.query(Class).filter(Class.id == id_class).first(),
            db_sess.query(Subjects).filter(Subjects.id == id_subject).first())
    students = sorted(db_sess.query(Student).filter(Student.id_class == id_class).all(), key=lambda x: x.surname)
    dates = list(map(lambda x: x[0].strftime('%d.%m.%Y'),
                     sorted(db_sess.query(Marks.date).filter((Marks.id_subject == id_subject),
                                                             (date1 < Marks.date), (date2 > Marks.date)).distinct())))
    marks = {}
    sr_marks = {}
    res_marks = {}
    for student in students:
        marks[student.id] = {}
        sum_mark = 0
        col_mark = 0
        for mark in sorted(
                db_sess.query(Marks).filter(Marks.id_student == student.id, Marks.id_subject == id_subject,
                                            date1 < Marks.date, date2 > Marks.date).all(), key=lambda x: x.date):
            marks[student.id][mark.date.strftime('%d.%m.%Y')] = mark.mark
            m = mark.mark
            if type(m) == str:
                if m != 'н':
                    sum_mark += int(m[:-1])
                    col_mark += 1
            else:
                sum_mark += m
                col_mark += 1
        if col_mark != 0:
            sr_marks[student] = str(round(sum_mark / col_mark, 2))
            res_marks[student] = str(round(sum_mark / col_mark + 0.01))
        else:
            sr_marks[student] = str(0)
    return render_template('html/students.html', title='Оценки',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=form, students=students, marks=marks, form=submit_form, dates=dates, sr_marks=sr_marks,
                           res_marks=res_marks)


@app.route('/student_start', methods=['GET'])
def student_start():
    db_sess = db_session.create_session()
    class_id = db_sess.query(Student).filter(Student.id == current_user.id).first().id_class
    class1 = db_sess.query(Class).filter(Class.id == class_id).first()
    school_id = class1.id_school
    school = db_sess.query(School).filter(School.id == school_id).first()
    return render_template('html/student_start.html', title=f'{current_user.surname} {current_user.first_name}',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=[school.title, class1.title], student=current_user.id)


@app.route('/student_marks/<int:id_student>/<int:part>', methods=['GET'])
def student_marks(id_student, part):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id_student).first()
    lessons1 = db_sess.query(TeacherClass).filter(TeacherClass.id_class == student.id_class).all()
    lessons = []
    for i in lessons1:
        lessons.append(db_sess.query(Subjects).filter(Subjects.id == i.id_subject).first())
    lessons = sorted(lessons, key=lambda x: x.title)
    marks = {}
    sr_marks = {}
    res_marks = {}
    date1, date2 = date_division(part)
    dates = list(map(lambda x: x[0].strftime('%d.%m.%Y'),
                     sorted(db_sess.query(Marks.date).filter((Marks.id_student == student.id),
                                                             (date1 < Marks.date), (date2 > Marks.date)).distinct())))
    for lesson in lessons:
        marks[lesson.id] = {}
        sum_mark = 0
        col_mark = 0
        for mark in sorted(db_sess.query(Marks).filter(Marks.id_student == student.id,
                                                       date1 < Marks.date, date2 > Marks.date).all(),
                           key=lambda x: x.date):
            marks[lesson.id][mark.date.strftime('%d.%m.%Y')] = mark.mark
            m = mark.mark
            if type(m) == str:
                if m != 'н':
                    sum_mark += int(m[:-1])
                    col_mark += 1
            else:
                sum_mark += m
                col_mark += 1
        if col_mark != 0:
            sr_marks[student] = str(round(sum_mark / col_mark, 2))
            res_marks[student] = str(round(sum_mark / col_mark + 0.01))
        else:
            sr_marks[student] = str(0)
    return render_template('html/student_marks.html', logo=student,
                           user=f'{student.first_name[0]}. {student.last_name[0]}. {student.surname}',
                           title=f'Оценки, {student.surname} {student.first_name}', marks=marks, dates=dates,
                           sr_marks=sr_marks, res_marks=res_marks, lessons=lessons)


@app.route('/timetable/<logo>', methods=['GET'])
def timetable(logo):
    db_sess = db_session.create_session()
    lessons = db_sess.query(SubjectPlan).filter(SubjectPlan.id_class == current_user.id_class).all()
    timetable = [{} for _ in range(6)]
    logo = logo[2:-2].split(',')
    logo = logo[0][:-1] + ', ' + logo[1][2:]
    for i in lessons:
        timetable[i.day - 1][i.lesson] = db_sess.query(Subjects).filter(i.id_subject == Subjects.id).first().title
    return render_template('html/timetable.html', title='Расписание уроков',
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
    return render_template('html/final_marks.html', title='Итоговые оценки',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=logo, marks=[s1, s2, s3, s4, s5])


@app.route('/student_profile', methods=['GET', 'POST'])
def student_profile():
    form = EditFormS()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Student).filter(Student.id == current_user.id).first()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.surname = form.surname.data
        user.id_school = db_sess.query(School).filter(School.title == form.school.data).first().id
        user.id_class = db_sess.query(Class).filter(Class.title == form.class1.data).first().id
        user.login = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.surname = form.surname.data
        current_user.id_school = db_sess.query(School).filter(School.title == form.school.data).first().id
        current_user.id_class = db_sess.query(Class).filter(Class.title == form.class1.data).first().id
        current_user.login = form.email.data
        db_sess.commit()
        return redirect('/student_start')
    return render_template('html/student_profile.html', title='Профиль', form=form, user=current_user)


@app.route('/change_part/<int:id_class>/<int:id_subject>', methods=['GET'])
def change_part(id_class, id_subject):
    db_sess = db_session.create_session()
    school = db_sess.query(School).filter(School.id == current_user.id_school).first().title
    class1 = db_sess.query(Class).filter(Class.id == id_class).first().title
    return render_template('html/change_part.html', title='Выбор четверти', logo=school, class1=[id_class, id_subject],
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           class2=class1)


@app.route('/result_marks/<int:id_class>/<int:id_subject>', methods=['GET', 'POST'])
def result_marks(id_class, id_subject):
    db_sess = db_session.create_session()
    submit_form = SaveMarkF()
    if submit_form.validate_on_submit():
        db_sess = db_session.create_session()
        mark = db_sess.query(FinalMarks).filter(FinalMarks.id_student == submit_form.id_student.data,
                                                FinalMarks.id_subject == id_subject,
                                                FinalMarks.part == submit_form.part.data).first()
        mark.mark = submit_form.mark.data
        db_sess.commit()
        return redirect(f'/result_marks/{id_class}/{id_subject}')
    form = (db_sess.query(Class).filter(Class.id == id_class).first(),
            db_sess.query(Subjects).filter(Subjects.id == id_subject).first())
    students = sorted(db_sess.query(Student).filter(Student.id_class == id_class).all(), key=lambda x: x.surname)
    marks = {}
    res_marks = {}
    for student in students:
        marks[student.id] = {}
        sum_marks = 0
        for mark in db_sess.query(FinalMarks).filter(FinalMarks.id_student == student.id,
                                                     FinalMarks.id_subject == id_subject).all():
            marks[student.id][mark.part] = mark.mark
            sum_marks += mark.mark
        res_marks[student] = str(round(sum_marks / 4 + 0.01))
    return render_template('html/result_marks.html', title='Итоговые оценки',
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           logo=form, students=students, marks=marks, form=submit_form, res_marks=res_marks)


@app.route('/change_part_s/<int:id_student>', methods=['GET'])
def change_part_s(id_student):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id_student).first()
    class1 = db_sess.query(Class).filter(Class.id == student.id_class).first()
    school = db_sess.query(School).filter(School.id == class1.id_school).first()
    return render_template('html/change_part_s.html', title='Выбор четверти', logo=school.title + ', ' + class1.title,
                           student=student,
                           user=f'{current_user.first_name[0]}. {current_user.last_name[0]}. {current_user.surname}',
                           class2=class1)


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')



