from flask import render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import Blog, User, Comment
from .forms import CommentForm, BlogForm, UpdateProfile
from flask_login import login_user,login_required,current_user,logout_user
from ..request import get_quote

@main.route('/')
def index():   
   """Fetch the blogs from the database"""  
   quote = get_quote() 
   blogs = Blog.query.all()
   print(blogs)
   return render_template('index.html', blogs = blogs, quote = quote)

@main.route('/comment/<int:id>',methods = ['GET','POST'])
def comment(id):
   """
   Allow for commenting of a given blog.
   """
   #Should return a blog by id   
   a_blog = Blog.query.filter_by(id= id)
   print(a_blog)
   
   #return comments per blog
   comments = Comment.query.filter_by(blog_id =id)
   print(comments)
   
   form = CommentForm()   
   new_comment = Comment()
   
   if form.validate_on_submit():
      new_comment.comment_msg = form.comment_msg.data
      new_comment.blog_id = id

      db.session.add(new_comment)
      db.session.commit()
   
   return render_template('comment.html',a_blog = a_blog, comment_form=form, comments = comments)

@main.route('/blog/')
def blog():
   """
   path for creating a new blog
   """
   return render_template('blog.html')

@main.route('/user/<uname>')
def profile(uname):   
   # blogs = Blog.query.all()
   blogs = Blog.query.filter_by(user_id = current_user.id)
   print(blogs)
   
   user = User.query.filter_by(username = uname).first()
   if user is None:
      abort(404)

   return render_template("profile/profile.html", user = user, blogs= blogs)
   
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
   user = User.query.filter_by(username = uname).first()
   if user is None:
      abort(404)

   form = UpdateProfile()

   if form.validate_on_submit():
      user.bio = form.bio.data

      db.session.add(user)
      db.session.commit()

      return redirect(url_for('.profile',uname=user.username))

   return render_template('profile/update.html',form =form)
 
@main.route('/user/<uname>/write Blog',methods = ['GET','POST'])
@login_required
def write_blog(uname):
   new_blog = Blog()
   
   user = User.query.filter_by(username = uname).first()
   if user is None:
      abort(404)

   form = BlogForm()

   if form.validate_on_submit():
      new_blog.title = form.title.data
      new_blog.blog_msg = form.blog_msg.data
      new_blog.user_id = current_user.id

      db.session.add(new_blog)
      db.session.commit()

      return redirect(url_for('.profile',uname=user.username))

   return render_template("writeblog.html",form =form)
 