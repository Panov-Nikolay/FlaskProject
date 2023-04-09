import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Marks(SqlAlchemyBase):
    __tablename__ = 'marks'
    student_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date)
    lesson = sqlalchemy.Column(sqlalchemy.Integer)  # <--- номер урока в конкретный день
    subject_id = sqlalchemy.Column(sqlalchemy.Integer)  # <--- id учебного предмета
    mark = sqlalchemy.Column(sqlalchemy.String)  # <--- от 2 до 5; String для поддержки "-" и "+"
