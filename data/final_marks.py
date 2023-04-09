import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class FinalMarks(SqlAlchemyBase):
    __tablename__ = 'final_marks'
    student_id = sqlalchemy.Column(sqlalchemy.Integer)
    part = sqlalchemy.Column(sqlalchemy.String)  # <--- четверть / полугодие / год == a / b / c + её номер
    # a2 = вторая четверть; b1 = первое полугодие
    subject_id = sqlalchemy.Column(sqlalchemy.Integer)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
