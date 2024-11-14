from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st


class Workflow_Task(Base):
    __tablename__ = 'workflow_tasks'
    id = Column(Integer, primary_key=True)
    owner = Column(String(32))
    workflow_id = Column(Integer)
    experiment_id = Column(Integer)
    dataset_id = Column(String(4096))
    knowledge_id = Column(Integer)
    dataset_content = Column(Text)
    character = Column(Text)
    entity_model_content = Column(Text)
    entity_extract = Column(Text)
    entity_extract_parse = Column(Text)
    attribute_model_content = Column(Text)
    attribute_extract = Column(Text)
    attribute_extract_parse = Column(Text)
    relation_model_content = Column(Text)
    relation_extract = Column(Text)
    relation_extract_parse = Column(Text)
    entity_extract_result = Column(Text)
    attribute_extract_result = Column(Text)
    relation_extract_result = Column(Text)
    start_at = Column(DateTime)
    finish_at = Column(DateTime)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Workflow_Task, self).__init__(**kwargs)

    @staticmethod
    def get_workflow_tasks_by_workflow_id(workflow_id):
        return session.query(Workflow_Task).filter(Workflow_Task.workflow_id == workflow_id).all()

    @staticmethod
    def get_workflow_task_by_id(id):
        return session.query(Workflow_Task).filter(Workflow_Task.id == id).first()

    def __repr__(self):
        return '<Workflow_Task %r>' % self.id

