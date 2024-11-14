import streamlit as st
from web.database.prompt import Prompt
from web.database import session

st.header('提示词创建')
st.session_state.current_page = 'prompt_create_page'

my_prompts = []
for prompt in Prompt.get_all_prompts():
    my_prompts.append('{}: 【{}】 【{}】'.format(prompt.id, prompt.owner, prompt.name))
prompt_select = st.selectbox('选择提示词基线', options=my_prompts)

prompt_character = ''
prompt_entity_extract = ''
prompt_entity_extract_parse = ''
prompt_attribute_extract = ''
prompt_attribute_extract_parse = ''
prompt_relation_extract = ''
prompt_relation_extract_parse = ''

if prompt_select is not None:
    prompt_id = prompt_select.split(':')[0]
    prompt = Prompt.get_prompt_by_id(prompt_id)
    prompt_character = prompt.character
    prompt_entity_extract = prompt.entity_extract
    prompt_entity_extract_parse = prompt.entity_extract_parse
    prompt_attribute_extract = prompt.attribute_extract
    prompt_attribute_extract_parse = prompt.attribute_extract_parse
    prompt_relation_extract = prompt.relation_extract
    prompt_relation_extract_parse = prompt.relation_extract_parse

with st.form('submit'):
    character = st.text_area('角色扮演', value=prompt_character, height=240, max_chars=4096, disabled=True)

    entity, attribute, relation = st.tabs(["实体抽取", "属性抽取", "关系抽取"])
    with entity:
        entity_extract = st.text_area('实体抽取', value=prompt_entity_extract, height=240, max_chars=4096, disabled=True)
        entity_extract_parse = st.text_area('实体结果解析', value=prompt_entity_extract_parse, height=120, max_chars=4096,
                                            disabled=True)
    with attribute:
        attribute_extract = st.text_area('属性抽取', value=prompt_attribute_extract, height=240, max_chars=4096,
                                         disabled=True)
        attribute_extract_parse = st.text_area('属性结果解析', value=prompt_attribute_extract_parse, height=120,
                                               max_chars=4096, disabled=True)
    with relation:
        relation_extract = st.text_area('关系抽取', value=prompt_relation_extract, height=240, max_chars=4096,
                                        disabled=True)
        relation_extract_parse = st.text_area('关系结果解析', value=prompt_relation_extract_parse, height=120,
                                              max_chars=4096, disabled=True)

    prompt_name = st.text_input('提示词名', key='prompt_name')
    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if Prompt.get_prompt_by_owner_with_name(prompt_name) is not None:
            st.error('用户下已有同名提示词，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            prompt_id = prompt_select.split(':')[0]
            try:
                Prompt.create_from_base(prompt_name, prompt_id)
                st.success('提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')
