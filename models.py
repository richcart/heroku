import os

from sqlalchemy import Column, String, create_engine, Integer, PickleType, Date
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
# database_path = 'postgres://qzwlkfgdgbtujl:67a8458a8ada7b6c90594c45df6354e9ec910e5b2c2a7df413970a846a1a5fe0@ec2-3-91-139-25.compute-1.amazonaws.com:5432/defl22mrhoku1u'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''


roles = db.Table('roles',
                 db.Column('actor_id', db.Integer, db.ForeignKey('actors.id')),
                 db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
                 )


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    gender = Column(String)
    movies = db.relationship('Movie',
                             secondary=roles,
                             backref=db.backref('movies')
                             )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, name, catchphrase=""):
        self.name = name
        self.catchphrase = catchphrase

    def format(self):
        return {

        }