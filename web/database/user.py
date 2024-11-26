from web.database import Base, Session
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
    def create_user(user):
        try:
            session = Session()
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_user_by_username(username):
        try:
            session = Session()
            return session.query(User).filter(User.username == username).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_user_by_id(id):
        try:
            session = Session()
            return session.query(User).filter(User.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_user_by_email(email):
        try:
            session = Session()
            return session.query(User).filter(User.email == email).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_password(self, password):
        try:
            session = Session()
            self.password = password
            self.update_at = datetime.now()
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_email(self, email):
        try:
            session = Session()
            self.email = email
            self.update_at = datetime.now()
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<User %r>' % self.username
