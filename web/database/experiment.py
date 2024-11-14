from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    owner = Column(String(32))
    prompt_id = Column(Integer)
    model_ids = Column(String(64))
    entity_extract_model_id = Column(Integer)
    attribute_extract_model_id = Column(Integer)
    relation_extract_model_id = Column(Integer)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Experiment, self).__init__(**kwargs)

    @staticmethod
    def get_experiments_by_owner():
        return session.query(Experiment).filter(Experiment.owner == st.session_state.current_username).all()

    @staticmethod
    def get_experiment_by_id(id):
        return session.query(Experiment).filter(Experiment.id == id).first()

    @staticmethod
    def get_experiment_by_owner_with_name(name):
        return session.query(Experiment).filter(Experiment.owner == st.session_state.current_username, Experiment.name == name).first()

    def __repr__(self):
        return '<Workflow %r>' % self.name

