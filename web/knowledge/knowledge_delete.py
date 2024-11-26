import streamlit as st
from web.database.knowledge import Knowledge
from web.tools.knowledge import get_knowledge_stats

st.header('知识库删除')
st.session_state.current_page = 'knowledge_delete_page'

with st.form('submit'):
    my_knowledges = []
    for knowledge in Knowledge.get_knowledges_by_owner():
        my_knowledges.append('{}: 【{}】 【{}】'.format(knowledge.id, knowledge.catalog, knowledge.name))
    knowledge_select = st.selectbox('选择知识库', options=my_knowledges)

    if knowledge_select is not None:
        knowledge_id = knowledge_select.split(':')[0]
        knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
        entities_cnt, attributes_cnt, relations_cnt = get_knowledge_stats(knowledge.rdf_xml_online)
        with st.container(border=True):
            st.text('实体个数：{}'.format(entities_cnt))
            st.text('属性个数：{}'.format(attributes_cnt))
            st.text('关系个数：{}'.format(relations_cnt))
            st.text('更新时间：{}'.format(knowledge.update_at))

    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if knowledge_select is None:
            st.error('知识库不能为空，请选择知识库！', icon=':material/error:')
            error = True
        if not error:
            try:
                Knowledge.delete_knowledge_by_id(knowledge_id)
                st.success('知识库删除成功！', icon=':material/done:')
            except Exception as e:
                st.error('知识库删除失败，错误原因：{}！'.format(e), icon=':material/error:')
