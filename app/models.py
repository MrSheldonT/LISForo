from datetime import datetime
from app import db

class Role(db.Model):
    __tablename__ = 'roles'
    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum('admin', 'user', name='role_name'), nullable=False, unique=True)

class User(db.Model):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False, unique=True)
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id_role', ondelete='RESTRICT', onupdate='CASCADE'))

    role = db.relationship('Role', backref='users')

class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE', onupdate='CASCADE') )
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user =  db.relationship('User', backref='posts')

class Comment(db.Model):
    __tablename__ = "comments"
    id_comment = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, db.ForeignKey('posts.id_post', ondelete='CASCADE', onupdate='CASCADE'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE', onupdate='CASCADE'))
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    is_edited = db.Column(db.Boolean, nullable=True)
    post = db.relationship('Post', backref='comments')
    user = db.relationship('User', backref='comments')

class CommentLike(db.Model):
    __tablename__ = "comment_likes"
    id_comment_like = db.Column(db.Integer, primary_key=True)
    id_comment = db.Column(db.Integer, db.ForeignKey('comments.id_comment', ondelete='CASCADE', onupdate='CASCADE'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE', onupdate='CASCADE') )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.relationship('Comment', backref='likes')
    user = db.relationship('User', backref='comment_likes')

class PostLike(db.Model):
    __tablename__ = "post_likes"
    id_post_like = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, db.ForeignKey('posts.id_post', ondelete='CASCADE', onupdate='CASCADE'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE', onupdate='CASCADE') )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.relationship('Post', backref='likes')
    user = db.relationship('User', backref='post_likes')