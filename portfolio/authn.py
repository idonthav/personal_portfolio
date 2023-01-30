from flask import Blueprint, render_template, redirect, url_for, request, flash
from portfolio import db
from portfolio.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 'authn module' has all view functions asscociated with user-authentication: signup/login/logout
authn = Blueprint("authn", __name__)

# ----------------------------------------- signup ----------------------------------------------
'''
Code adapted from Youtube example:
https://www.youtube.com/watch?v=M_OKJnIdYeU
'''

@authn.route("/sign-up", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")     # singup.html 'name=email'
        username = request.form.get("username")  # singup.html 'name=username'
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # email id unique
        email_register = User.query.filter_by(email=email).all()
        username_register = User.query.filter_by(username=username).all()
        '''
        Code adapted from a post on Stack Overflow forum:
        https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
        '''
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid emial address',category='error')
        elif email_register:
            flash('email is registered already', category='error')
        elif username_register:
            flash('username is taken already', category='error')
        elif password1 != password2:
            flash('passwords are not same', category='error')
        else:
            '''
            werkzeug.security adapted from a post from TANXY on 20220410 and <FLASK_3_EXERCISE>:
            https://tanxy.club/2022/encryption-algorithms-in-flask
            '''
            new_user = User(email = email, username=username, password=generate_password_hash(password1))  # bydefault: method='sha256'
            # add new_user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully', category='success')
            return redirect(url_for('about.home'))

    return render_template("signup.html", user_email=current_user)


# ----------------------------------------- login ----------------------------------------------
'''
Code adapted from Youtube example:
https://www.youtube.com/watch?v=W4GItcW7W-U&t=696s
'''

@authn.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")   # login.html 'name=email'
        password = request.form.get("password")   # login.html 'name=password'
        
        user_email = User.query.filter_by(email=email).first()
        if user_email:
            if check_password_hash(user_email.password, password):
                flash('You have logged in successfully', category='success')
                login_user(user_email, remember=True)
                return redirect(url_for('about.home'))
            else:
                flash("Emial or password is not right", category="error")
        else:
            flash("Not exist", category='error')

    return render_template("login.html", user_email=current_user)


# ----------------------------------------- logout ----------------------------------------------
'''
Code adapted from Youtube example:
https://www.youtube.com/watch?v=W4GItcW7W-U&t=696s
'''

# no need of a HTML page, just need to redirect to Login
@authn.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have logged out', category='success')
    return redirect(url_for("authn.login"))