from datetime import UTC, datetime
from blog import db, login_manager
from flask import current_app
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # This didn't work
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Here the attributes of the class User and Post represent the 
# columns in our database tables.

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)  # Note that this is not a column
    # If you see this is a table you won't see this as column.
    # Also note that we passed the class name "Post" as argument
    # One user may have many posts
    # The backref argument is like adding another column in the Post model named author

    def __repr__(self):  # string representation (used for debugging and testing)
        return f"User('{self.username}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'].encode('utf-8'), expires_sec)
        return s.dumps({'user_id': self.id}, b'itsdangerous').encode('utf-8') # this solved the error of trying to '+' int and byte type ( we converted salt to byte).
    
    @staticmethod  # This makes sure that the below method doesn't expect the self as the first argument, which it normally does being a class's method
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)  # returns the User object (which also contains email of that particular user) with the given user_id.        


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Note that we have passed the table name and column name unlike the argument passed 
    # to the relationship method in the User class.
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.published_date}')"