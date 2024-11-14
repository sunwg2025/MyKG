from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    owner = Column(String(32))
    content = Column(Text)
    is_default = Column(Boolean)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    @staticmethod
    def get_base_models():
        all_bases = session.query(Model).filter(Model.owner == 'system').all()
        if st.session_state.current_username != 'system':
            all_bases.extend(session.query(Model).filter(Model.owner == st.session_state.current_username).all())
        return all_bases

    @staticmethod
    def get_models_by_owner():
        return session.query(Model).filter(Model.owner == st.session_state.current_username).all()

    @staticmethod
    def get_default_model_by_owner():
        return session.query(Model).filter(Model.owner == st.session_state.current_username, Model.is_default).first()

    @staticmethod
    def get_model_by_owner_with_name(name):
        return session.query(Model).filter(Model.owner == st.session_state.current_username, Model.name == name).first()

    @staticmethod
    def get_model_by_id(id):
        return session.query(Model).filter(Model.id == id).first()

    @staticmethod
    def get_model_by_id_list(id_list):
        models = []
        for id in id_list:
            models.append(Model.get_model_by_id(id))
        print(models)
        return models

    @staticmethod
    def clear_default_model_by_owner():
        default_model = Model.get_default_model_by_owner()
        if default_model:
            default_model.is_default = False
            default_model.update_at = datetime.now()
            session.commit()

    def update_model_columns(self, new):
        self.name = new.name
        self.content = new.content
        self.is_default = new.is_default
        self.update_at = datetime.now()
        session.commit()

    @staticmethod
    def delete_model_by_id(id):
        model = session.query(Model).filter(Model.id == id).first()
        session.delete(model)
        session.commit()

    def __repr__(self):
        return '<Model %r>' % self.name