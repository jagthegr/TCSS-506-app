from datetime import datetime  # Added datetime
from flask_sqlalchemy import SQLAlchemy # This line was present but flask_sqlalchemy is not directly used here, db is. Keeping for now.
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager # Import db and login_manager from the app package

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128)) # Kept 128 from the models.py version
    decks = db.relationship('Deck', backref='author', lazy='dynamic') # Added decks relationship

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card', backref='deck', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Deck {self.title}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    def __repr__(self):
        return f'<Card {self.id} Q: {self.question[:20]}...>'