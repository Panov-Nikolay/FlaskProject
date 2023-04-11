import sqlalchemy
from .db_session import SqlAlchemyBase


class TeacherClass(SqlAlchemyBase):
    __tablename__ = 'teacher_class'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
    id_subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subject.id'))
