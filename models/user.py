from flask_login import UserMixin
from models.database import db


class User(UserMixin, db.Model):
    """Model class for representing users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    reset_password = db.Column(db.Integer, default=0)
    isAdmin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, isAdmin=False):
        self.username = username
        self.password = password
        self.email = email
        self.isAdmin = isAdmin

    def __repr__(self):
        """Representation of the User object."""
        return f"User(id={self.id}, username={self.username}, isAdmin={self.isAdmin})"

    def serialize(self):
        """Serialize user object."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'isAdmin': self.isAdmin
        }
