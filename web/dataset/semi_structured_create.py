import streamlit as st
from web.database.dataset import Dataset
from web.database.model import Model
from web.tools.model import analyze_content_tags
from io import StringIO

st.header('半结构化数据集创建')

st.session_state.current_page = 'semi_structured_create_page'


type = st.radio('选择创建类型', ['单文件', '多文件'], horizontal=True)