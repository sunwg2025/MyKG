from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


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
    def create_experiment(experiment):
        try:
            session = Session()
            session.add(experiment)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_experiments_by_owner():
        try:
            session = Session()
            return session.query(Experiment).filter(Experiment.owner == st.session_state.current_username).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_experiment_by_id(id):
        try:
            session = Session()
            return session.query(Experiment).filter(Experiment.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_experiment_by_owner_with_name(name):
        try:
            session = Session()
            return session.query(Experiment).filter(Experiment.owner == st.session_state.current_username,
                                                    Experiment.name == name).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    def update_experiment_attribute_extract_model_id(self, attribute_extract_model_id):
        try:
            session = Session()
            self.attribute_extract_model_id = attribute_extract_model_id
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_experiment_entity_extract_model_id(self, entity_extract_model_id):
        try:
            session = Session()
            self.entity_extract_model_id = entity_extract_model_id
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_experiment_relation_extract_model_id(self, relation_extract_model_id):
        try:
            session = Session()
            self.relation_extract_model_id = relation_extract_model_id
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Workflow %r>' % self.name

