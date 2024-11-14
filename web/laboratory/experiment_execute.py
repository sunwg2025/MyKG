import streamlit as st
from web.database.model import Model
from web.database.prompt import Prompt
from web.database.experiment import Experiment

st.header('知识构建实验执行')
st.session_state.current_page = 'experiment_execute_page'

st.subheader('Step 1：选择实验', divider=True)
with st.container(border=True):
    my_experiments = []
    index = 0
    select_index = 0
    for experiment in Experiment.get_experiments_by_owner():
        if 'current_experiment_id' in st.session_state:
            if int(experiment.id) == int(st.session_state.current_experiment_id):
                select_index = index
            index += 1
        my_experiments.append('{}: 【{}】'.format(experiment.id, experiment.name))
    experiment_select = st.selectbox('选择实验', options=my_experiments, index=select_index)

    if experiment_select is not None:
        experiment_id = experiment_select.split(':')[0]
        if 'current_experiment_id' not in st.session_state:
            st.session_state.current_experiment_id = experiment_id
        else:
            st.session_state.current_experiment_id = experiment_id
        experiment = Experiment.get_experiment_by_id(experiment_id)
        prompt = Prompt.get_prompt_by_id(experiment.prompt_id)
        st.session_state['entity_extract_prompt'] = prompt.entity_extract
        if experiment.entity_extract_model_id is not None:
            entity_extract_model = Model.get_model_by_id(experiment.entity_extract_model_id)
            st.session_state['entity_extract_model'] = entity_extract_model.name
        else:
            st.session_state['entity_extract_model'] = ''
        st.session_state['attribute_extract_prompt'] = prompt.attribute_extract
        if experiment.attribute_extract_model_id is not None:
            attribute_extract_model = Model.get_model_by_id(experiment.attribute_extract_model_id)
            st.session_state['attribute_extract_model'] = attribute_extract_model.name
        else:
            st.session_state['attribute_extract_model'] = ''
        st.session_state['relation_extract_prompt'] = prompt.relation_extract
        if experiment.relation_extract_model_id is not None:
            relation_extract_model = Model.get_model_by_id(experiment.relation_extract_model_id)
            st.session_state['relation_extract_model'] = relation_extract_model.name
        else:
            st.session_state['relation_extract_model'] = ''

st.subheader('Step 2：实体抽取实验', divider=True)
entity_extract_prompt = st.text_area('实体抽取提示词', height=240, max_chars=4096, key='entity_extract_prompt')
entity_extract_model = st.text_input('实体抽取模型', key='entity_extract_model')
st.page_link('web/knowledge_extract/entity_extract.py', label='跳转-实体抽取实验', icon=':material/nat:')

st.subheader('Step 3：属性抽取实验', divider=True)
attribute_extract_prompt = st.text_area('属性抽取提示词', height=240, max_chars=4096, key='attribute_extract_prompt')
attribute_extract_model = st.text_input('属性抽取模型', key='attribute_extract_model')
st.page_link('web/knowledge_extract/attribute_extract.py', label='跳转-属性抽取实验', icon=':material/nat:')

st.subheader('Step 4：关系抽取实验', divider=True)
relation_extract_prompt = st.text_area('关系抽取提示词', height=240, max_chars=4096, key='relation_extract_prompt')
relation_extract_model = st.text_input('关系抽取模型', key='relation_extract_model')
st.page_link('web/knowledge_extract/relation_extract.py', label='跳转-关系抽取实验', icon=':material/nat:')