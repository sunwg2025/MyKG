import streamlit as st
from web.database.model import Model
from web.database.experiment import Experiment
from web.database.prompt import Prompt
from web.database import session
from web.database.workflow import Workflow

st.header('知识构建实验')
st.session_state.current_page = 'experiment_create_page'

character_value = ''
entity_extract_value = ''
entity_extract_parse_value = ''
attribute_extract_value = ''
attribute_extract_parse_value = ''
relation_extract_value = ''
relation_extract_parse_value = ''

st.subheader('Step 1：选择提示词', divider=True)
with st.container(border=True):
    my_prompts = []
    for prompt in Prompt.get_prompts_by_owner():
        my_prompts.append('{}: 【{}】'.format(prompt.id, prompt.name))
    prompt_select = st.selectbox('选择提示词', options=my_prompts)

    if prompt_select is not None:
        prompt_id = prompt_select.split(':')[0]
        prompt = Prompt.get_prompt_by_id(prompt_id)
        character_value = prompt.character
        entity_extract_value = prompt.entity_extract
        entity_extract_parse_value = prompt.entity_extract_parse
        attribute_extract_value = prompt.attribute_extract
        attribute_extract_parse_value = prompt.attribute_extract_parse
        relation_extract_value = prompt.relation_extract
        relation_extract_parse_value = prompt.relation_extract_parse

    character = st.text_area('角色扮演', value=character_value, height=240, max_chars=4096, key='character')
    entity, attribute, relation = st.tabs(["实体抽取", "属性抽取", "关系抽取"])
    with entity:
        entity_extract = st.text_area('实体抽取', value=entity_extract_value, height=240, max_chars=4096, key='entity_extract')
        entity_extract_parse = st.text_area('结果解析', value=entity_extract_parse_value, height=120, max_chars=4096, key='entity_extract_parse')
    with attribute:
        attribute_extract = st.text_area('属性抽取', value=attribute_extract_value, height=240, max_chars=4096, key='attribute_extract')
        attribute_extract_parse = st.text_area('结果解析', value=attribute_extract_parse_value, height=120, max_chars=4096, key='attribute_extract_parse')
    with relation:
        relation_extract = st.text_area('关系抽取', value=relation_extract_value, height=240, max_chars=4096, key='relation_extract')
        relation_extract_parse = st.text_area('结果解析', value=relation_extract_parse_value, height=120, max_chars=4096, key='relation_extract_parse')


st.subheader('Step 2：选择备选模型', divider=True)
with st.container(border=True):
    my_models = []
    for model in Model.get_base_models():
        my_models.append('{}: 【{}】【{}】'.format(model.id, model.owner, model.name))
    models_select = st.multiselect('选择模型', options=my_models, max_selections=5)

    if len(models_select) > 0:
        tabs = st.tabs(models_select)

        for i, tab in enumerate(tabs):
            with tab:
                model_id = models_select[i].split(':')[0]
                model = Model.get_model_by_id(model_id)
                model_content = st.text_area('', value=model.content, height=240, max_chars=4096, key=model_id)

st.subheader('Step 3：创建实验', divider=True)
with st.container(border=True):
    experiment_name = st.text_input('实验名', key='experiment_name')

    if st.button('提交'):
        error = False
        if prompt_select is None:
            st.error('提示词不能为空，请重新输入！', icon=':material/error:')
            error = True
        if len(models_select) == 0 and not error:
            st.error('模型不能为空，请重新输入！', icon=':material/error:')
            error = True
        if Experiment.get_experiment_by_owner_with_name(experiment_name) is not None and not error:
            st.error('用户下已有同名实验，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                prompt_id = prompt_select.split(':')[0]
                model_ids = []
                for model_select in models_select:
                    model_ids.append(model_select.split(':')[0])
                experiment = Experiment(name=experiment_name,
                                        owner=st.session_state.current_username,
                                        prompt_id=prompt_id,
                                        model_ids=str(model_ids))
                session.add(experiment)
                session.commit()
                st.success('知识实验创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('知识实验创建失败，错误原因：{}！'.format(e), icon=':material/error:')