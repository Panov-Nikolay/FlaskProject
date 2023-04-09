import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class SubjectPlan(SqlAlchemyBase):
    __tablename__ = 'subject_plan'
    subject_id = sqlalchemy.Column(sqlalchemy.Integer)
    day = sqlalchemy.Column(sqlalchemy.Integer)  # <--- день недели (1 - понедельник, 7 - воскресенье)
    lesson = sqlalchemy.Column(sqlalchemy.Integer)  # <--- номер урока в расписании в конкретный день
    class_id = sqlalchemy.Column(sqlalchemy.Integer)
