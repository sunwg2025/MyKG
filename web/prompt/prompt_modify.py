import streamlit as st
from web.database.prompt import Prompt

st.header('提示词变更')
st.session_state.current_page = 'prompt_modify_page'

my_prompts = []
for prompt in Prompt.get_prompts_by_owner():
    my_prompts.append('{}: 【{}】'.format(prompt.id, prompt.name))
prompt_select = st.selectbox('选择提示词', options=my_prompts)

prompt_name = ''
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
    prompt_name = prompt.name
    prompt_character = prompt.character
    prompt_entity_extract = prompt.entity_extract
    prompt_entity_extract_parse = prompt.entity_extract_parse
    prompt_attribute_extract = prompt.attribute_extract
    prompt_attribute_extract_parse = prompt.attribute_extract_parse
    prompt_relation_extract = prompt.relation_extract
    prompt_relation_extract_parse = prompt.relation_extract_parse

with st.form("submit"):
    prompt_name_new = st.text_input('提示词名', value=prompt_name)
    character = st.text_area('角色扮演', value=prompt_character, height=480, max_chars=4096)

    entity, attribute, relation = st.tabs(["实体抽取", "属性抽取", "关系抽取"])
    with entity:
        entity_extract = st.text_area('提示词', value=prompt_entity_extract, height=360, max_chars=4096)
        entity_extract_parse = st.text_area('结果解析', value=prompt_entity_extract_parse, height=120, max_chars=4096,
                                            key='entity_extract_parse')
    with attribute:
        attribute_extract = st.text_area('提示词', value=prompt_attribute_extract, height=360, max_chars=4096,
                                         key='attribute_extract')
        attribute_extract_parse = st.text_area('结果解析', value=prompt_attribute_extract_parse, height=120,
                                               max_chars=4096, key='attribute_extract_parse')
    with relation:
        relation_extract = st.text_area('提示词', value=prompt_relation_extract, height=360, max_chars=4096,
                                        key='relation_extract')
        relation_extract_parse = st.text_area('结果解析', value=prompt_relation_extract_parse, height=120,
                                              max_chars=4096, key='relation_extract_parse')

    delete = st.toggle("删除")
    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if prompt_select is None:
            st.error('提示词选择不能为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            prompt_id = prompt_select.split(':')[0]
            if delete:
                try:
                    Prompt.delete_prompt_by_id(prompt_id)
                    st.success('提示词删除成功！', icon=':material/done:')
                except Exception as e:
                    st.error('提示词删除失败，错误原因：{}！'.format(e), icon=':material/error:')
            else:
                error = False
                if str(Prompt.get_prompt_by_owner_with_name(prompt_name_new).id) != str(prompt_id):
                    st.error('用户下已有同名提示词，请重新输入！', icon=':material/error:')
                    error = True
                if not error:
                    try:
                        prompt = Prompt.get_prompt_by_id(prompt_id)
                        new = Prompt(name=prompt_name_new,
                                     character=character,
                                     entity_extract=entity_extract,
                                     entity_extract_parse=entity_extract_parse,
                                     attribute_extract=attribute_extract,
                                     attribute_extract_parse=attribute_extract_parse,
                                     relation_extract=relation_extract,
                                     relation_extract_parse=relation_extract_parse)
                        prompt.update_prompt_columns(new)
                        st.success('提示词更新成功！', icon=':material/done:')
                    except Exception as e:
                        st.error('提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
