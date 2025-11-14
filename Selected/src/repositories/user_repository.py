from models.user import User
from db import db

class UserRepository:
    def get_by_email_or_username(self, email_or_username: str):
        return User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()

    def get_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_by_username(self, username: str):
        return User.query.filter_by(username=username).first()

    def create(self, email: str, username: str, password_hash: str):
        user = User(email=email, username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
