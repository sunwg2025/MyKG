from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    enabled = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def get_user_by_username(username):
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(id):
        return session.query(User).filter(User.id == id).first()

    @staticmethod
    def get_user_by_email(email):
        return session.query(User).filter(User.email == email).first()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_password(self, password):
        self.password = password
        self.update_at = datetime.now()
        session.commit()

    def update_email(self, email):
        self.email = email
        self.update_at = datetime.now()
        session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
