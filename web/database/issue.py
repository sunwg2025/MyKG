from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    page = Column(String(32))
    owner = Column(String(32))
    title = Column(String(256))
    detail = Column(String(4096))
    fixed = Column(Boolean, default=False)
    comment = Column(String(4096))
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Issue, self).__init__(**kwargs)

    @staticmethod
    def create_issue(issue):
        try:
            session = Session()
            session.add(issue)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_issues_by_id(id):
        try:
            session = Session()
            return session.query(Issue).filter(Issue.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_issues_by_owner():
        try:
            session = Session()
            return session.query(Issue).filter(Issue.owner == st.session_state.current_username).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_issues_by_fixed(fixed):
        try:
            session = Session()
            return session.query(Issue).filter(Issue.fixed == fixed).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    def update_issue_to_fixed(self, is_fixed, comment):
        try:
            session = Session()
            self.fixed = is_fixed
            self.comment = comment
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Issue %r>' % self.username
