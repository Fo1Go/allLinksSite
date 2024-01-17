from flask_login import UserMixin
from links import db, login_manager
from datetime import datetime


ROLES = {
    'admin': 'admin',
    'moder': 'moderator',
    'user': 'user',
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(80), nullable=False)
    links = db.relationship('Links', backref='owner', lazy=True)
    review = db.relationship('Reviews', backref='rater', lazy=True)
    role = db.relationship('Roles', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}")'


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Link("{self.link}")'


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Review("{self.title}", "{self.rating}")'
    

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_role = db.Column(db.String(20), nullable=False, default=ROLES['user'])

    def __repr__(self):
        return f'Role("{self.user_id}", "{self.user_role}")'
    

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Friend("{self.friend_id}")'
    

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(64), nullable=True, default='None')
    

    def __repr__(self):
        return f'News("{self.title}", "{self.date}")'