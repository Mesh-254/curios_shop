from models.database import db
from models.user import User
from app import app


with app.app_context():
    admin = User(username='admin', password='password', email='admin@gmail.com', isAdmin=True)
    db.session.add(admin)
    db.session.commit()
