import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class TeacherClass(SqlAlchemyBase):
    __tablename__ = 'teacher_class'
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer)
    class_id = sqlalchemy.Column(sqlalchemy.Integer)
