from web.database import Base, session
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
    def get_issues_by_id(id):
        return session.query(Issue).filter(Issue.id == id).first()

    @staticmethod
    def get_issues_by_owner():
        return session.query(Issue).filter(Issue.owner == st.session_state.current_username).all()

    @staticmethod
    def get_issues_by_fixed(fixed):
        return session.query(Issue).filter(Issue.fixed == fixed).all()

    def __repr__(self):
        return '<Issue %r>' % self.username
