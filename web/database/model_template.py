from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Model_Template(Base):
    __tablename__ = 'model_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    content = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Model_Template, self).__init__(**kwargs)

    @staticmethod
    def get_all_templates():
        return session.query(Model_Template).filter().all()

    @staticmethod
    def get_template_by_id(id):
        return session.query(Model_Template).filter(Model_Template.id == id).first()

    @staticmethod
    def get_template_by_name(name):
        return session.query(Model_Template).filter(Model_Template.name == name).first()

    def update_model_template_columns(self, new):
        self.name = new.name
        self.content = new.content
        self.update_at = datetime.now()
        session.commit()

    @staticmethod
    def delete_model_template_by_id(id):
        model_template = session.query(Model_Template).filter(Model_Template.id == id).first()
        session.delete(model_template)
        session.commit()

    def __repr__(self):
        return '<Model_Template %r>' % self.name