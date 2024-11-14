import streamlit as st
from web.database.knowledge import Knowledge
from web.tools.knowledge import get_knowledge_stats
from datetime import datetime
from web.database import session


st.header('知识库管理')
st.session_state.current_page = 'knowledge_manage_page'

with st.container(border=True):
    my_knowledges = []
    for knowledge in Knowledge.get_knowledges_by_owner():
        my_knowledges.append('{}: 【{}】 【{}】'.format(knowledge.id, knowledge.catalog, knowledge.name))
    knowledge_select = st.selectbox('选择知识库', options=my_knowledges)

    entities_cnt = 0
    attributes_cnt = 0
    relations_cnt = 0
    update_at = None
    entities_online_cnt = 0
    attributes_online_cnt = 0
    relations_online_cnt = 0
    update_at_online = None

    if knowledge_select is not None:
        knowledge_id = knowledge_select.split(':')[0]
        knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
        entities_cnt, attributes_cnt, relations_cnt = get_knowledge_stats(knowledge.rdf_xml)
        update_at = knowledge.update_at.strftime('%Y-%m-%d %H:%M:%S')
        entities_online_cnt, attributes_online_cnt, relations_online_cnt = get_knowledge_stats((knowledge.rdf_xml_online))
        update_at_online = knowledge.update_at_online.strftime('%Y-%m-%d %H:%M:%S')

    col1, col2, col3 = st.columns([0.41, 0.18, 0.41], vertical_alignment='center')
    with col1:
        with st.container(border=True):
            st.text('知识库-开发：')
            st.text('实体个数：{}'.format(entities_cnt))
            st.text('属性个数：{}'.format(attributes_cnt))
            st.text('关系个数：{}'.format(relations_cnt))
            st.text('更新时间：{}'.format(update_at))
    with col2:
        if st.button("知识库上线==>"):
            error = False
            if knowledge_select is None:
                st.error('知识库不能为空，请重新输入！', icon=':material/error:')
                error = True
            if not error:
                knowledge_id = knowledge_select.split(':')[0]
                knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
                knowledge.rdf_xml_online = knowledge.rdf_xml
                knowledge.update_at_online = datetime.now()
                session.commit()
                st.success('知识库上线成功！', icon=':material/done:')
        if st.button("知识库重载<=="):
            error = False
            if knowledge_select is None:
                st.error('知识库不能为空，请重新输入！', icon=':material/error:')
                error = True
            if not error:
                knowledge_id = knowledge_select.split(':')[0]
                knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
                knowledge.rdf_xml = knowledge.rdf_xml_online
                knowledge.update_at = datetime.now()
                session.commit()
                st.success('知识库重载成功！', icon=':material/done:')
    with col3:
        with st.container(border=True):
            st.text('知识库-生产：')
            st.text('实体个数：{}'.format(entities_online_cnt))
            st.text('属性个数：{}'.format(attributes_online_cnt))
            st.text('关系个数：{}'.format(relations_online_cnt))
            st.text('更新时间：{}'.format(update_at_online))