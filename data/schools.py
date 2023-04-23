import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class School(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_region = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('regions.id'))

    region = orm.relationship('Region', back_populates='schools')
    classes = orm.relationship('Class', back_populates='school')
    teachers = orm.relationship('Teacher', back_populates='school')
