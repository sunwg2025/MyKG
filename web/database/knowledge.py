from web.database import Base, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
import streamlit as st
from datetime import datetime


class Knowledge(Base):
	__tablename__ = 'knowledges'
	id = Column(Integer, primary_key=True)
	catalog = Column(String(64))
	name = Column(String(64))
	owner = Column(String(32))
	rdf_xml = Column(Text)
	update_at = Column(DateTime, default=func.datetime('now', 'localtime'))
	rdf_xml_online = Column(Text)
	update_at_online = Column(DateTime, default=func.datetime('now', 'localtime'))
	create_at = Column(DateTime, default=func.datetime('now', 'localtime'))


	def __init__(self, **kwargs):
		super(Knowledge, self).__init__(**kwargs)

	@staticmethod
	def create_knowledge(knowledge):
		try:
			session = Session()
			session.add(knowledge)
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	@staticmethod
	def get_knowledges_by_owner():
		try:
			session = Session()
			return session.query(Knowledge).filter(Knowledge.owner == st.session_state.current_username).all()
		except Exception as e:
			raise e
		finally:
			session.close()

	@staticmethod
	def get_knowledge_by_owner_with_name(name):
		try:
			session = Session()
			return session.query(Knowledge).filter(Knowledge.owner == st.session_state.current_username,
												   Knowledge.name == name).first()
		except Exception as e:
			raise e
		finally:
			session.close()

	@staticmethod
	def get_knowledge_by_owner_with_name_api(username, knowledge_name):
		try:
			session = Session()
			return session.query(Knowledge).filter(Knowledge.owner == username, Knowledge.name == knowledge_name).first()
		except Exception as e:
			raise e
		finally:
			session.close()

	@staticmethod
	def get_knowledge_by_id(id):
		try:
			session = Session()
			return session.query(Knowledge).filter(Knowledge.id == id).first()
		except Exception as e:
			raise e
		finally:
			session.close()

	@staticmethod
	def delete_knowledge_by_id(id):
		try:
			session = Session()
			knowledge = session.query(Knowledge).filter(Knowledge.id == id).first()
			session.delete(knowledge)
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	@staticmethod
	def update_knowledge_rdf_xml_online(id):
		try:
			session = Session()
			knowledge = session.query(Knowledge).filter(Knowledge.id == id).first()
			knowledge.rdf_xml_online = knowledge.rdf_xml
			knowledge.update_at_online = datetime.now()
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	@staticmethod
	def reload_knowledge_rdf_xml(id):
		try:
			session = Session()
			knowledge = session.query(Knowledge).filter(Knowledge.id == id).first()
			knowledge.rdf_xml = knowledge.rdf_xml_online
			knowledge.update_at = datetime.now()
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	def update_knowledge_rdf_xml(self, rdf_xml):
		try:
			session = Session()
			self.rdf_xml = rdf_xml
			self.update_at = datetime.now()
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	def __repr__(self):
		return '<Knowledge %r>' % self.name

