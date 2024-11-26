from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime


class Model_Template(Base):
    __tablename__ = 'model_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    content = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Model_Template, self).__init__(**kwargs)

    @staticmethod
    def create_model_template(model_template):
        try:
            session = Session()
            session.add(model_template)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_templates():
        try:
            session = Session()
            return session.query(Model_Template).filter().all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_template_by_id(id):
        try:
            session = Session()
            return session.query(Model_Template).filter(Model_Template.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_template_by_name(name):
        try:
            session = Session()
            return session.query(Model_Template).filter(Model_Template.name == name).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    def update_model_template_columns(self, new):
        try:
            session = Session()
            self.name = new.name
            self.content = new.content
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_model_template_by_id(id):
        try:
            session = Session()
            model_template = session.query(Model_Template).filter(Model_Template.id == id).first()
            session.delete(model_template)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Model_Template %r>' % self.name