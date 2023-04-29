import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))

    form = orm.relationship('Class', back_populates='students')
    marks = orm.relationship('Marks', back_populates='student')
    final_marks = orm.relationship('FinalMarks', back_populates='student')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
