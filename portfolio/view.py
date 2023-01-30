from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from portfolio import db
from portfolio.models import Post, User

'''
Code adapted from Youtube example and Flask Documentation:
https://www.youtube.com/watch?v=GQcM8wdduLI
https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
'''
about = Blueprint("about", __name__)

# user is able to access home.html after login
@about.route("/")
@login_required
def home():
    username = request.form.get("username")
    return render_template("home.html", user_email=current_user, name = current_user.username)
 

@about.route("/post-create", methods=['GET', 'POST'])
@login_required
def post_create():
    if request.method == 'POST':
        text = request.form.get('text')
        if len(text) < 5:
            flash('Message is at least 5 characters', category='error')
        else:
            post = Post(text=text, writer = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Message sent successfully', category='success')
           
    posts = Post.query.all()
    
    return render_template('post_create.html', user_email=current_user, posts=posts, username=current_user.username)

'''
Code adapted from <FLASK_2_EXERCISE> and Youtube example:
https://www.youtube.com/watch?v=M_OKJnIdYeU
'''
@about.route("/post-delete/<id>")
@login_required
def post_delete(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post is deleted successuflly', category='success')
    
    return redirect(url_for('about.post_create'))

    
    
