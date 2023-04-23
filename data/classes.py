import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_school = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('schools.id'))

    school = orm.relationship('School', back_populates='classes')
    students = orm.relationship('Student', back_populates='form')
