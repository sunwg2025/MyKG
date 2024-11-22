from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Dataset_Split(Base):
    __tablename__ = 'dataset_splits'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    owner = Column(String(32))
    dataset_id = Column(Integer)
    split_seq = Column(Integer)
    total_size = Column(Integer)
    content = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Dataset_Split, self).__init__(**kwargs)

    @staticmethod
    def get_dataset_splits_by_dataset_id(dataset_id):
        return session.query(Dataset_Split).filter(Dataset_Split.dataset_id == dataset_id)\
            .order_by(Dataset_Split.split_seq).all()

    @staticmethod
    def get_dataset_splits_by_id(id):
        return session.query(Dataset_Split).filter(Dataset_Split.id == id).first()

    @staticmethod
    def delete_dataset_split_by_id(id):
        dataset = session.query(Dataset_Split).filter(Dataset_Split.id == id).first()
        session.delete(dataset)
        session.commit()

    def __repr__(self):
        return '<Dataset_Split %r>' % self.name