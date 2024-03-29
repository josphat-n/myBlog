from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(UserMixin, db.Model):
   __tablename__ = 'users'

   id = db.Column(db.Integer,primary_key = True)
   username = db.Column(db.String(255),index = True)
   email = db.Column(db.String(255),unique = True,index = True)
   pass_secure = db.Column(db.String(255))  
   profile_pic_path = db.Column(db.String()) 
   bio = db.Column(db.String(255))
   password_hash = db.Column(db.String(255))
   blogs = db.relationship('Blog',backref = 'user',lazy="dynamic")
   
   @property
   def password(self):
      raise AttributeError('You cannot read the password attribute')

   @password.setter
   def password(self, password):
      self.pass_secure = generate_password_hash(password)

   def verify_password(self,password):
      return check_password_hash(self.pass_secure,password)    
   
   def __repr__(self):
      return f'User {self.username}'
   
class Blog(db.Model):
   __tablename__ = 'blogs'
   
   id = db.Column(db.Integer,primary_key = True)    
   title = db.Column(db.String(255))
   blog_msg =  db.Column(db.String(2000))
   user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
   comments = db.relationship('Comment',backref = 'blog',lazy="dynamic")
   
   def __repr__(self):

      return f'Pitch {self.blog_msg}'

class Comment(db.Model):
   __tablename__ = 'comments'
   
   id = db.Column(db.Integer,primary_key = True)    
   comment_msg =  db.Column(db.String(2000))
   blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))   
   
   @classmethod
   def get_comments(cls,id):
      comments = Comment.query.filter_by(blog_id = id).all()
      return comments   
   
   def __repr__(self):   
      return f'Comment {self.comment_msg}'
   
class Quote:
   """
   Blueprint for creating quote objects
   """
   
   def __init__(self, id, author, quote):
      self.id = id
      self.author = author
      self.quote = quote