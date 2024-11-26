from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Prompt(Base):
    __tablename__ = 'prompts'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    owner = Column(String(32))
    character = Column(Text)
    entity_extract = Column(Text)
    entity_extract_parse = Column(Text)
    attribute_extract = Column(Text)
    attribute_extract_parse = Column(Text)
    relation_extract = Column(Text)
    relation_extract_parse = Column(Text)
    create_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    update_at = Column(DateTime, default=func.datetime('now', 'localtime'))

    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)

    @staticmethod
    def create_prompt(prompt):
        try:
            session = Session()
            session.add(prompt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_prompts():
        try:
            session = Session()
            all_bases = session.query(Prompt).filter(Prompt.owner == 'system').all()
            if st.session_state.current_username != 'system':
                all_bases.extend(session.query(Prompt).filter(Prompt.owner == st.session_state.current_username).all())
            return all_bases
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_prompts_by_owner():
        try:
            session = Session()
            return session.query(Prompt).filter(Prompt.owner == st.session_state.current_username).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_prompt_by_owner_with_name(name):
        try:
            session = Session()
            return session.query(Prompt).filter(Prompt.owner == st.session_state.current_username,
                                                Prompt.name == name).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def get_prompt_by_id(id):
        try:
            session = Session()
            return session.query(Prompt).filter(Prompt.id == id).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def create_from_base(name, base_id):
        try:
            session = Session()
            base = session.query(Prompt).filter(Prompt.id == base_id).first()
            prompt = Prompt(name=name,
                            owner=st.session_state.current_username,
                            character=base.character,
                            entity_extract=base.entity_extract,
                            entity_extract_parse=base.entity_extract_parse,
                            attribute_extract=base.attribute_extract,
                            attribute_extract_parse=base.attribute_extract_parse,
                            relation_extract=base.relation_extract,
                            relation_extract_parse=base.relation_extract_parse)
            session.add(prompt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_prompt_columns(self, new):
        try:
            session = Session()
            self.name = new.name
            self.character = new.character
            self.entity_extract = new.entity_extract
            self.entity_extract_parse = new.entity_extract_parse
            self.attribute_extract = new.attribute_extract
            self.attribute_extract_parse = new.attribute_extract_parse
            self.relation_extract = new.relation_extract
            self.relation_extract_parse = new.relation_extract_parse
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_prompt_by_id(id):
        try:
            session = Session()
            config = session.query(Prompt).filter(Prompt.id == id).first()
            session.delete(config)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_prompt_attribute_extract(self, attribute_extract):
        try:
            session = Session()
            self.attribute_extract = attribute_extract
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_prompt_entity_extract(self, entity_extract):
        try:
            session = Session()
            self.entity_extract = entity_extract
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_prompt_relation_extract(self, relation_extract):
        try:
            session = Session()
            self.relation_extract = relation_extract
            self.update_at = datetime.now()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def __repr__(self):
        return '<Prompt %r>' % self.name
