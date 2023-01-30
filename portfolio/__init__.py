from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


'''
Code of app instance adapted from Youtube and Flask Documentation
https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/
https://www.youtube.com/watch?v=W4GItcW7W-U
'''
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ="dhiehiwmcpep"
    '''
    Code of MySQL adapted from <FLASK_4_EXERCISE>
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21136510:Mybfiscute77!@csmysql.cs.cf.ac.uk:3306/c21136510_flask_lab_db'
    db.init_app(app)   

    '''
    Code adapted from <FLASK_3_EXERCISES> and Youtube example:
    https://www.youtube.com/watch?v=dam0GPOAvVI&t=7311s
    '''
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "authn.login"   # if someone not login, should redirect to Login

    # link view fucntions in Blueprint in view.py with application
    from portfolio.view import about
    app.register_blueprint(about) 

    from portfolio.authn import authn
    app.register_blueprint(authn)

    # import User model from models
    from portfolio.models import User
    from portfolio.models import Post

    with app.app_context():
        db.create_all()

    
    

    '''
    Code adapted from <FLASK_3_EXERCISES>
    '''
    # create function that allow LoginMnr find User model
    @login_manager.user_loader
    def loadUser(id):
        return User.query.get(int(id))


    return app



