from web.database import Base, Session
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
    def create_dataset_split_batch(dataset_splits):
        try:
            session = Session()
            for dataset_split in dataset_splits:
                session.add(dataset_split)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_dataset_splits_by_dataset_id(dataset_id):
        try:
            session = Session()
            return session.query(Dataset_Split).filter(Dataset_Split.dataset_id == dataset_id)\
                .order_by(Dataset_Split.split_seq).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_dataset_splits_by_id(id):
        try:
            session = Session()
            return session.query(Dataset_Split).filter(Dataset_Split.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_dataset_split_by_id(id):
        try:
            session = Session()
            dataset = session.query(Dataset_Split).filter(Dataset_Split.id == id).first()
            session.delete(dataset)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Dataset_Split %r>' % self.name