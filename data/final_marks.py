import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class FinalMarks(SqlAlchemyBase):
    __tablename__ = 'final_marks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_student = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id'))
    part = sqlalchemy.Column(sqlalchemy.Integer)
    id_subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    mark = sqlalchemy.Column(sqlalchemy.Integer)

    student = orm.relationship('Student', back_populates='final_marks')
