from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class System_Prompt(Base):
    __tablename__ = 'system_prompts'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    content = Column(Text)
    result = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(System_Prompt, self).__init__(**kwargs)

    @staticmethod
    def get_system_prompt_by_name(name):
        return session.query(System_Prompt).filter(System_Prompt.name == name).first()

    @staticmethod
    def update_system_prompt_by_name(name, content, result):
        system_prompt = System_Prompt.get_system_prompt_by_name(name)
        system_prompt.content = content
        system_prompt.result = result
        system_prompt.update_at = datetime.now()
        session.commit()


    def __repr__(self):
        return '<System_Prompt %r>' % self.name


