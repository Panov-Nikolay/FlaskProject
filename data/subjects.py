import sqlalchemy
from .db_session import SqlAlchemyBase


class Subjects(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)