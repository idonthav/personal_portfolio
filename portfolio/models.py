from portfolio import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import bcrypt

'''
Code adapted from <FLASK_2_EXERCISE: P-13> and Youtube example:
https://www.youtube.com/watch?v=W4GItcW7W-U&t=640s
'''

# -------------------------------  User Schema  -----------------------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(800), unique=True)
    password = db.Column(db.String(2000))
    d1 = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', lazy=True)

    '''
    Code adapted from <FLASK_2_EXERCISE: P-13> and a post from Stack Overflow on 20180213
    https://stackoverflow.com/questions/48761260/bcrypt-encoding-error
    '''
   
    

# -------------------------------  Post Schema  -----------------------------------------------

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable = True)
    d1 = db.Column(db.DateTime(timezone=True), default=func.now())
    writer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
