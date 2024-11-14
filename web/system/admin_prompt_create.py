import streamlit as st
from web.database.prompt import Prompt
from web.database import session


st.header('系统提示词创建')
st.session_state.current_page = 'admin_prompt_create_page'

with st.form('submit'):
    character = st.text_area('角色扮演', height=240, max_chars=4096, key='character')

    entity, attribute, relation = st.tabs(["实体抽取", "属性抽取", "关系抽取"])
    with entity:
        entity_extract = st.text_area('实体抽取', height=240, max_chars=4096, key='entity_extract')
        entity_extract_parse = st.text_area('结果解析', height=120, max_chars=4096, key='entity_extract_parse')
    with attribute:
        attribute_extract = st.text_area('属性抽取', height=240, max_chars=4096, key='attribute_extract')
        attribute_extract_parse = st.text_area('结果解析', height=120, max_chars=4096, key='attribute_extract_parse')
    with relation:
        relation_extract = st.text_area('关系抽取', height=240, max_chars=4096, key='relation_extract')
        relation_extract_parse = st.text_area('结果解析', height=120, max_chars=4096, key='relation_extract_parse')

    prompt_name = st.text_input('提示词名', key='prompt_name')
    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if Prompt.get_prompt_by_owner_with_name(prompt_name) is not None:
            st.error('用户下已有同名提示词，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                prompt = Prompt(name=prompt_name,
                                owner=st.session_state.current_username,
                                character=character,
                                entity_extract=entity_extract,
                                entity_extract_parse=entity_extract_parse,
                                attribute_extract=attribute_extract,
                                attribute_extract_parse=attribute_extract_parse,
                                relation_extract=relation_extract,
                                relation_extract_parse=relation_extract_parse)
                session.add(prompt)
                session.commit()
                st.success('提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')
