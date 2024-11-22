from web.database import Base, session
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
	def get_knowledges_by_owner():
		return session.query(Knowledge).filter(Knowledge.owner == st.session_state.current_username).all()

	@staticmethod
	def get_knowledge_by_owner_with_name(name):
		return session.query(Knowledge).filter(Knowledge.owner == st.session_state.current_username, Knowledge.name == name).first()

	@staticmethod
	def get_knowledge_by_owner_with_name_api(username, knowledge_name):
		return session.query(Knowledge).filter(Knowledge.owner == username, Knowledge.name == knowledge_name).first()

	@staticmethod
	def get_knowledge_by_id(id):
		return session.query(Knowledge).filter(Knowledge.id == id).first()

	@staticmethod
	def delete_knowledge_by_id(id):
		knowledge = session.query(Knowledge).filter(Knowledge.id == id).first()
		session.delete(knowledge)
		session.commit()

	def __repr__(self):
		return '<Knowledge %r>' % self.name

