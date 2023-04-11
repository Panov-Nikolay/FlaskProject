import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class TeacherClass(SqlAlchemyBase):
    __tablename__ = 'teacher_class'

    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
