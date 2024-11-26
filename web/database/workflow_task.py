from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime


class Workflow_Task(Base):
    __tablename__ = 'workflow_tasks'
    id = Column(Integer, primary_key=True)
    owner = Column(String(32))
    workflow_id = Column(Integer)
    experiment_id = Column(Integer)
    dataset_id = Column(Integer)
    dataset_split_id = Column(Integer)
    knowledge_id = Column(Integer)
    dataset_split_name = Column(String(64))
    dataset_split_content = Column(Text)
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
    def create_workflow_tasks_batch(workflow_tasks_batch):
        try:
            session = Session()
            for workflow_task in workflow_tasks_batch:
                session.add(workflow_task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_workflow_tasks_by_workflow_id(workflow_id):
        try:
            session = Session()
            return session.query(Workflow_Task).filter(Workflow_Task.workflow_id == workflow_id).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_workflow_task_by_id(id):
        try:
            session = Session()
            return session.query(Workflow_Task).filter(Workflow_Task.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def clear_workflow_task_by_id(id):
        try:
            session = Session()
            workflow_task = Workflow_Task.get_workflow_task_by_id(id)
            workflow_task.entity_extract_result = None
            workflow_task.attribute_extract_result = None
            workflow_task.relation_extract_result = None
            workflow_task.start_at = None
            workflow_task.finish_at = None
            workflow_task.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_workflow_task(self, entity_extract_result, attribute_extract_result, relation_extract_result, task_start_at):
        try:
            session = Session()
            self.entity_extract_result = str(entity_extract_result)
            self.attribute_extract_result = str(attribute_extract_result)
            self.relation_extract_result = str(relation_extract_result)
            self.start_at = task_start_at
            self.finish_at = datetime.now()
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Workflow_Task %r>' % self.id

