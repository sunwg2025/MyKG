from web.database import Base, session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func


class Experiment_Log(Base):
    __tablename__ = 'experiment_logs'
    id = Column(Integer, primary_key=True)
    owner = Column(String(32))
    experiment_id = Column(Integer)
    type = Column(String(16))
    dataset_id = Column(Integer)
    model_id = Column(Integer)
    extract_prompt = Column(Text)
    extract_result = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Experiment_Log, self).__init__(**kwargs)

    @staticmethod
    def get_experiment_logs_by_experiment_id(experiment_id):
        return session.query(Experiment_Log).filter(Experiment_Log.experiment_id == experiment_id).all()

    @staticmethod
    def get_experiment_logs_by_experiment_id_and_type(experiment_id, type):
        return session.query(Experiment_Log).filter(Experiment_Log.experiment_id == experiment_id, Experiment_Log.type == type).all()

    def __repr__(self):
        return '<Experiment_Log %r>' % self.id

