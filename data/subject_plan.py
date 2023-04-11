import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class SubjectPlan(SqlAlchemyBase):
    __tablename__ = 'subject_plan'

    id_subject = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    day = sqlalchemy.Column(sqlalchemy.Integer)  # <--- день недели (1 - понедельник, 7 - воскресенье)
    lesson = sqlalchemy.Column(sqlalchemy.Integer)  # <--- номер урока в расписании в конкретный день
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
