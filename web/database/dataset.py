from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    catalog = Column(String(64))
    name = Column(String(64))
    owner = Column(String(32))
    channel = Column(String(32))
    source = Column(String(2048))
    tags = Column(String(64))
    total_size = Column(Integer)
    split_count = Column(Integer)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Dataset, self).__init__(**kwargs)

    @staticmethod
    def get_datasets_by_owner():
        return session.query(Dataset).filter(Dataset.owner == st.session_state.current_username).all()

    @staticmethod
    def get_dataset_by_id(id):
        return session.query(Dataset).filter(Dataset.id == id).first()

    @staticmethod
    def get_dataset_by_id_list(id_list):
        datasets = []
        for id in id_list:
            datasets.append(Dataset.get_dataset_by_id(id))
        return datasets

    @staticmethod
    def get_dataset_by_owner_with_name(name):
        return session.query(Dataset).filter(Dataset.owner == st.session_state.current_username, Dataset.name == name).first()

    @staticmethod
    def get_catalogs_by_owner():
        catalogs = []
        datasets = Dataset.get_datasets_by_owner()
        for dataset in datasets:
            catalogs.append(dataset.catalog)
        return list(set(catalogs))

    def update_dataset_columns(self, new):
        self.catalog = new.catalog
        self.name = new.name
        self.tags = new.tags
        self.update_at = datetime.now()
        session.commit()

    @staticmethod
    def delete_dataset_by_id(id):
        dataset = session.query(Dataset).filter(Dataset.id == id).first()
        session.delete(dataset)
        session.commit()

    def __repr__(self):
        return '<Dataset %r>' % self.name