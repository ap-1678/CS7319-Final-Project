from werkzeug.security import generate_password_hash, check_password_hash
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def signup(self, email: str, username: str, password: str):
        if self.repo.get_by_email(email):
            raise ValueError("Email already in use.")
        if self.repo.get_by_username(username):
            raise ValueError("Username already in use.")
        pw_hash = generate_password_hash(password)
        user = self.repo.create(email=email, username=username, password_hash=pw_hash)
        return user

    def login(self, email_or_username: str, password: str):
        user = self.repo.get_by_email_or_username(email_or_username)
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials.")
        return user
