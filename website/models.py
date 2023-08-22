from . import db
from flask_login import UserMixin
from sqlalchemy import func


# The Note class represents a user's note in the database.
class Note(db.Model):
    # The id attribute is the primary key for the Note table.
    id = db.Column(db.Integer, primary_key=True)

    # The title attribute stores the title of the note.
    title = db.Column(db.String(150))

    # The data attribute stores the original file data of the note.
    data = db.Column(db.LargeBinary)

    # The content attribute stores the extracted text from the note file.
    content = db.Column(db.String(10000))

    # The date attribute stores the date and time when the note was created.
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # The user_id attribute is a foreign key that references the id of the user who created the note.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# The User class represents a user account in the database.
class User(db.Model, UserMixin):
    # The id attribute is the primary key for the User table.
    id = db.Column(db.Integer, primary_key=True)

    # The email attribute stores the email address of the user.
    email = db.Column(db.String(150), unique=True)

    # The password attribute stores the password of the user.
    password = db.Column(db.String(150))

    # The username attribute stores the username of the user.
    username = db.Column(db.String(150))

    # The notes attribute is a relationship that represents all notes created by this user.
    notes = db.relationship('Note')
