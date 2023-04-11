import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class FinalMarks(SqlAlchemyBase):
    __tablename__ = 'final_marks'

    id_student = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id'))
    part = sqlalchemy.Column(sqlalchemy.String)  # <--- четверть / полугодие / год == a / b / c + её номер
    # a2 = вторая четверть; b1 = первое полугодие
    id_subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    mark = sqlalchemy.Column(sqlalchemy.Integer)
