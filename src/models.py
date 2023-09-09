from . import db
from flask_login import UserMixin
from sqlalchemy import func
import datetime


# The Note class represents a user's note in the database.
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    data = db.Column(db.LargeBinary)
    content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))


# The Note class represents a user's note in the database.
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.relationship('Note', backref='folder')


# The Test class represents a user's saved tests in the database.
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    questions = db.Column(db.PickleType)
    guesses = db.Column(db.PickleType)
    answers = db.Column(db.PickleType)
    question_types = db.Column(db.PickleType)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.title = 'test ' + str(datetime.datetime.now())


# The User class represents a user account in the database.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    open_question_pref = db.Column(db.Integer)
    true_or_false_pref = db.Column(db.Integer)
    closed_question_pref = db.Column(db.Integer)
    language = db.Column(db.String(2))
    notes = db.relationship('Note')
    tests = db.relationship('Test')
    folders = db.relationship('Folder')
