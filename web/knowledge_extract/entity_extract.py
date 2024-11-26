import streamlit as st
from web.database.model import Model
from web.database.experiment import Experiment
from web.database.dataset import Dataset
from web.database.dataset_split import Dataset_Split
from web.database.prompt import Prompt
from web.tools.model import extract_entity_knowledge
from web.database.experiment_log import Experiment_Log

st.header('实体抽取实验')

if 'entity_extract_results' not in st.session_state:
    st.session_state.entity_extract_results = {}

if 'entity_extract_prompt_reload' not in st.session_state:
    st.session_state.entity_extract_prompt_reload = False

if 'entity_extract_prompt_history' not in st.session_state:
    st.session_state.entity_extract_prompt_history = ''

current_page = 'entity_extract_page'
if st.session_state.current_page != current_page:
    st.session_state.entity_extract_results = {}
st.session_state.current_page = current_page

if 'current_experiment_id' not in st.session_state:
    st.error('请从知识实验执行入口进入！', icon=':material/error:')
else:
    experiment = Experiment.get_experiment_by_id(st.session_state.current_experiment_id)
    prompt = Prompt.get_prompt_by_id(experiment.prompt_id)
    models = Model.get_model_by_id_list(eval(experiment.model_ids))

    st.selectbox('当前知识实验', options=['{}: 【{}】'.format(experiment.id, experiment.name)], disabled=True)

    st.subheader('Step 1：选择数据集和模型', divider=True)
    with st.container(border=True):
        my_datasets = []
        for dataset in Dataset.get_datasets_by_owner():
            my_datasets.append('{}: 【{}】 【{}】'.format(dataset.id, dataset.catalog, dataset.name))
        dataset_select = st.selectbox('选择数据集', options=my_datasets)

        if dataset_select is not None:
            dataset_id = dataset_select.split(':')[0]
            dataset = Dataset.get_dataset_by_id(dataset_id)

            dataset_splits = []
            for dataset_split in Dataset_Split.get_dataset_splits_by_dataset_id(dataset_id):
                dataset_splits.append('{}: 数据分片【{}】 字符数【{}】'.format(dataset_split.id, dataset_split.name,
                                                                    dataset_split.total_size))
            dataset_split_select = st.selectbox('数据内容', options=dataset_splits)

            if dataset_split_select is not None:
                dataset_split_id = dataset_split_select.split(':')[0]
                dataset_split = Dataset_Split.get_dataset_splits_by_id(dataset_split_id)
                st.text_area('数据内容', height=360, max_chars=4096, value=dataset_split.content, disabled=True)

        models_data = []
        for model in models:
            models_data.append('{}: 【{}】'.format(model.id, model.name))
        models_select = st.multiselect('选择模型', options=models_data, max_selections=3)

    st.subheader('Step 2：编辑提示词', divider=True)
    with st.container(border=True):
        col1, col2 = st.columns([0.9, 0.1], vertical_alignment='bottom')
        with col1:
            if st.session_state.entity_extract_prompt_reload:
                st.session_state['extract_prompt'] = prompt.entity_extract
                st.session_state.entity_extract_prompt_reload = False
            if st.session_state.entity_extract_prompt_history != '':
                st.session_state['extract_prompt'] = st.session_state.entity_extract_prompt_history
                st.session_state.entity_extract_prompt_history = ''
            extract_prompt = st.text_area('提示词', height=360, max_chars=4096, key='extract_prompt')
        with col2:
            if st.button('载入默认'):
                st.session_state.entity_extract_prompt_reload = True
                st.rerun()


            @st.dialog('执行记录', width='large')
            def logs_view():
                data = []
                experiment_logs = Experiment_Log.get_experiment_logs_by_experiment_id_and_type(
                    st.session_state.current_experiment_id, 'entity_extract')
                for experiment_log in experiment_logs:
                    dataset = Dataset.get_dataset_by_id(experiment_log.dataset_id)
                    model = Model.get_model_by_id(experiment_log.model_id)
                    data.append({'重载': False, '执行时间': experiment_log.create_at, '数据集': dataset.name, '模型': model.name,
                                 '提示词': experiment_log.extract_prompt, '抽取结果': experiment_log.extract_result})

                column_config = {
                    '重载': st.column_config.CheckboxColumn('重载', width='small'),
                    '执行时间': st.column_config.DatetimeColumn('执行时间', disabled=True, width='small'),
                    '数据集': st.column_config.TextColumn('数据集', disabled=True, width='small'),
                    '模型': st.column_config.TextColumn('模型', disabled=True, width='small'),
                    '提示词': st.column_config.TextColumn('提示词', disabled=True, width='large', help='点击以查看完整数据'),
                    '抽取结果': st.column_config.TextColumn('抽取结果', disabled=True, width='large', help='点击以查看完整数据')
                }
                edited_datas = st.data_editor(data, column_config=column_config, hide_index=False, num_rows='fixed',
                                              use_container_width=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button('重载提示词'):
                        error = False
                        extract_prompts = []
                        for edited_data in edited_datas:
                            if edited_data['重载']:
                                extract_prompts.append(edited_data['提示词'])
                        if len(extract_prompts) == 0:
                            st.error('请选择需要重载的记录！', icon=':material/error:')
                            error = True
                        if len(extract_prompts) > 1 and not error:
                            st.error('选择的重载记录超过1条，请重新选择！', icon=':material/error:')
                            error = True
                        if not error:
                            st.session_state.entity_extract_prompt_history = extract_prompts[0]
                with col2:
                    if st.button('关闭'):
                        st.rerun()


            if st.button('载入历史'):
                t = logs_view()

    st.subheader('Step 3：执行实体抽取', divider=True)
    if st.button('抽取知识'):
        st.session_state.entity_extract_results = {}
        error = False
        if dataset_select is None:
            st.error('请选择数据集后在执行抽取！', icon=':material/error:')
            error = True
        if len(models_select) == 0 and not error:
            st.error('请选择模型后在执行抽取！', icon=':material/error:')
            error = True
        if not error:
            progress_text = '抽取中，请等待...'
            my_bar = st.progress(0, text=progress_text)

            if len(models_select) > 0:
                my_bar_progress = 1 / len(models_select)

            index = 1
            with st.container(border=True):
                for model_select in models_select:
                    model_id = model_select.split(':')[0]
                    model = Model.get_model_by_id(model_id)

                    extract_result = extract_entity_knowledge(dataset_content=dataset_split.content,
                                                              model_content=model.content,
                                                              character=prompt.character,
                                                              extract_prompt=extract_prompt,
                                                              extract_parse=prompt.entity_extract_parse)
                    result_key = '{}: {}'.format(model.id, model.name)
                    st.session_state.entity_extract_results[result_key] = extract_result

                    dataset_id = dataset_select.split(':')[0]
                    experiment_log = Experiment_Log(owner=st.session_state.current_username,
                                                    experiment_id=experiment.id,
                                                    type='entity_extract',
                                                    dataset_id=dataset_id,
                                                    dataset_split_id=dataset_split.id,
                                                    model_id=model_id,
                                                    extract_prompt=extract_prompt,
                                                    extract_result=str(extract_result))
                    Experiment_Log.create_experiment_log(experiment_log)

                    my_bar.progress(my_bar_progress * index, text=progress_text)
                    index += 1
            my_bar.empty()

    with st.form('submit'):
        for key in st.session_state.entity_extract_results.keys():
            st.text_area('抽取结果：{}'.format(key), height=240, max_chars=4096,
                         value=st.session_state.entity_extract_results[key], key=key)

        result_select = st.radio('选择抽取结果', options=st.session_state.entity_extract_results.keys())
        save_prompt = st.toggle('更新提示词')

        submit_button = st.form_submit_button('提交')
        if submit_button:
            error = False
            if save_prompt:
                try:
                    prompt.update_prompt_entity_extract(extract_prompt)
                except Exception as e:
                    error = True
                    st.error('提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
            if not error:
                try:
                    experiment.update_experiment_entity_extract_model_id(result_select.split(':')[0])
                    st.success('知识实验更新成功！', icon=':material/done:')
                except Exception as e:
                    error = True
                    st.error('知识实验更新失败，错误原因：{}！'.format(e), icon=':material/error:')

            st.session_state.entity_extract_results = {}

    st.page_link('web/laboratory/experiment_execute.py', label="跳转-知识实验执行", icon=':material/nat:')
