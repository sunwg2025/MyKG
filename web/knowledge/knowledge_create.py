import streamlit as st
from web.database.knowledge import Knowledge
from web.database import session
from web.tools.knowledge import get_knowledge_stats
import pandas as pd

st.header('知识库创建')
st.session_state.current_page = 'knowledge_create_page'

type = st.radio('选择创建类型', ['新创建空库', '从其他库继承'], horizontal=True)
if type == '新创建空库':
    with st.form('type1'):
        empty_rdf_xml = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
</rdf:RDF>"""
        catalog_name_1 = st.text_input('知识库类目', key='catalog_name_1')
        knowledge_name_1 = st.text_input('知识库名', key='knowledge_name_1')

        submit_button_1 = st.form_submit_button('提交')
        if submit_button_1:
            error = False
            if Knowledge.get_knowledge_by_owner_with_name(knowledge_name_1) is not None:
                st.error('用户下同名知识库已存在，请重新输入！', icon=':material/error:')
                error = True
            if not error:
                try:
                    knowledge = Knowledge(catalog=catalog_name_1,
                                          name=knowledge_name_1,
                                          owner=st.session_state.current_username,
                                          rdf_xml=empty_rdf_xml,
                                          rdf_xml_online=empty_rdf_xml)
                    session.add(knowledge)
                    session.commit()
                    st.success('知识库创建成功！', icon=':material/done:')
                except Exception as e:
                    session.rollback()
                    st.error('知识库创建失败，错误原因：{}！'.format(e), icon=':material/error:')

else:
    with st.form('type2'):
        my_knowledges = []
        for knowledge in Knowledge.get_knowledges_by_owner():
            my_knowledges.append('{}: 【{}】 【{}】'.format(knowledge.id, knowledge.catalog, knowledge.name))

        knowledge_select = st.selectbox('选择源知识库', options=my_knowledges)

        if knowledge_select is not None:
            base_knowledge_id = knowledge_select.split(':')[0]
            base_knowledge = Knowledge.get_knowledge_by_id(base_knowledge_id)
            entities_cnt, attributes_cnt, relations_cnt = get_knowledge_stats(base_knowledge.rdf_xml_online)
            with st.container(border=True):
                st.text('实体个数：{}'.format(entities_cnt))
                st.text('属性个数：{}'.format(attributes_cnt))
                st.text('关系个数：{}'.format(relations_cnt))
                st.text('更新时间：{}'.format(base_knowledge.update_at))

        catalog_name_2 = st.text_input('知识库类目', key='catalog_name_2')
        knowledge_name_2 = st.text_input('知识库名', key='knowledge_name_2')

        submit_button_2 = st.form_submit_button('提交')
        if submit_button_2:
            error = False
            if Knowledge.get_knowledge_by_owner_with_name(knowledge_name_2) is not None:
                st.error('用户下同名知识库已存在，请重新输入！', icon=':material/error:')
                error = True
            if not error:
                base_knowledge_id = knowledge_select.split(':')[0]
                rdf_xml_online = Knowledge.get_knowledge_by_id(base_knowledge_id).rdf_xml_online
                try:
                    knowledge = Knowledge(catalog=catalog_name_2,
                                          name=knowledge_name_2,
                                          owner=st.session_state.current_username,
                                          rdf_xml=rdf_xml_online,
                                          rdf_xml_online=rdf_xml_online)
                    session.add(knowledge)
                    session.commit()
                    st.success('知识库创建成功！', icon=':material/done:')
                except Exception as e:
                    session.rollback()
                    st.error('知识库创建失败，错误原因：{}！'.format(e), icon=':material/error:')
