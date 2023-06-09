import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Marks(SqlAlchemyBase):
    __tablename__ = 'marks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_student = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id'))
    date = sqlalchemy.Column(sqlalchemy.Date)
    id_subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    mark = sqlalchemy.Column(sqlalchemy.String)  # <--- от 2 до 5; String для поддержки "-" и "+"

    student = orm.relationship('Student', back_populates='marks')

