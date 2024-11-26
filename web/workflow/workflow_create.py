import streamlit as st
from web.database.experiment import Experiment
from web.database.model import Model
from web.database.dataset import Dataset
from web.database.dataset_split import Dataset_Split
from web.database.prompt import Prompt
from web.database.knowledge import Knowledge
from web.database.workflow import Workflow
from web.database.workflow_task import Workflow_Task
from web.tools.knowledge import load_knowledge_from_xml, get_all_entity_knowledge, get_all_attribute_knowledge
from web.tools.knowledge import get_all_relation_knowledge

st.header('工作流创建')
st.session_state.current_page = 'workflow_create_page'

st.subheader('Step 1：选择实验', divider=True)
with st.container(border=True):
    my_experiments = []
    for experiment in Experiment.get_experiments_by_owner():
        my_experiments.append('{}: 【{}】'.format(experiment.id, experiment.name))
    experiment_select = st.selectbox('选择实验', options=my_experiments)

    if experiment_select is not None:
        experiment_id = experiment_select.split(':')[0]
        experiment = Experiment.get_experiment_by_id(experiment_id)

        prompt = Prompt.get_prompt_by_id(experiment.prompt_id)

        prompt_select = st.text('提示词：{}'.format(prompt.name))
        if experiment.entity_extract_model_id is not None:
            entity_extract_model = Model.get_model_by_id(experiment.entity_extract_model_id)
            entity_extract_model_select = st.text('实体抽取模型：{}'.format(entity_extract_model.name))
        else:
            entity_extract_model_select = st.text('实体抽取模型：{}'.format('未配置'))
        if experiment.attribute_extract_model_id is not None:
            attribute_extract_model = Model.get_model_by_id(experiment.attribute_extract_model_id)
            attribute_extract_model_select = st.text('属性抽取模型：{}'.format(attribute_extract_model.name))
        else:
            attribute_extract_model_select = st.text('属性抽取模型：{}'.format('未配置'))
        if experiment.relation_extract_model_id is not None:
            relation_extract_model = Model.get_model_by_id(experiment.relation_extract_model_id)
            relation_extract_model_select = st.text('关系抽取模型：{}'.format(relation_extract_model.name))
        else:
            relation_extract_model_select = st.text('关系抽取模型：{}'.format('未配置'))

st.subheader('Step 2：选择数据集', divider=True)
with st.container(border=True):
    my_dataset_catalogs = Dataset.get_catalogs_by_owner()
    dataset_catalogs_select = st.multiselect('选择数据类目', options=my_dataset_catalogs)

    my_datasets = []
    for dataset in Dataset.get_datasets_by_owner():
        if len(dataset_catalogs_select) > 0:
            if dataset.catalog in dataset_catalogs_select:
                my_datasets.append('{}: 【{}】 【{}】'.format(dataset.id, dataset.catalog, dataset.name))
        else:
            my_datasets.append('{}: 【{}】 【{}】'.format(dataset.id, dataset.catalog, dataset.name))
    datasets_select = st.multiselect('选择数据集', options=my_datasets)

    dataset_size = 0
    dataset_split_cnt = 0
    dataset_ids = []
    for dataset_select in datasets_select:
        dataset_id = dataset_select.split(':')[0]
        dataset_ids.append(dataset_id)
        dataset = Dataset.get_dataset_by_id(dataset_id)
        dataset_split_cnt += dataset.split_count
        dataset_size += dataset.total_size
    datasets_count_text = st.text('数据集个数：{}'.format(len(datasets_select)))
    dataset_splits_count_text = st.text('数据分片个数：{}'.format(dataset_split_cnt))
    datasets_size_text = st.text('数据集总字符：{}'.format(dataset_size))

st.subheader('Step 3：选择知识库', divider=True)
with st.container(border=True):
    my_knowledges = []
    for knowledge in Knowledge.get_knowledges_by_owner():
        my_knowledges.append('{}: 【{}】 【{}】'.format(knowledge.id, knowledge.catalog, knowledge.name))
    knowledge_select = st.selectbox('选择知识库', options=my_knowledges)

    if knowledge_select is not None:
        knowledge_id = knowledge_select.split(':')[0]
        knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
        graph = load_knowledge_from_xml(knowledge.rdf_xml)
        entities_count_text = st.text('实体个数：{}'.format(len(get_all_entity_knowledge(graph))))
        attributes_count_text = st.text('属性个数：{}'.format(len(get_all_attribute_knowledge(graph))))
        relations_count_text = st.text('关系个数：{}'.format(len(get_all_relation_knowledge(graph))))

st.subheader('Step 4：创建工作流', divider=True)
with st.container(border=True):
    workflow_name = st.text_input('工作流名', key='workflow_name')

    if st.button('提交'):
        error = False
        if experiment_select is None:
            st.error('知识实验不能为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            experiment_id = experiment_select.split(':')[0]
            experiment = Experiment.get_experiment_by_id(experiment_id)
            if experiment.entity_extract_model_id is None and not error:
                st.error('知识实验-实体抽取未完成，请完成实验！', icon=':material/error:')
                error = True
            if experiment.attribute_extract_model_id is None and not error:
                st.error('知识实验-属性抽取未完成，请完成实验！', icon=':material/error:')
                error = True
            if experiment.relation_extract_model_id is None and not error:
                st.error('知识实验-关系抽取未完成，请完成实验！', icon=':material/error:')
                error = True
        if len(datasets_select) == 0 and not error:
            st.error('数据集不能为空，请重新输入！', icon=':material/error:')
            error = True
        if knowledge_select is None and not error:
            st.error('知识库不能为空，请重新输入！', icon=':material/error:')
            error = True
        if workflow_name is None and not error:
            st.error('工作流名不能为空，请重新输入！', icon=':material/error:')
            error = True
        if Workflow.get_workflow_by_owner_name(workflow_name) is not None and not error:
            st.error('已存在同名工作流，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                knowledge_id = knowledge_select.split(':')[0]

                workflow = Workflow(name=workflow_name,
                                    owner=st.session_state.current_username,
                                    experiment_id=experiment.id,
                                    dataset_ids=str(dataset_ids),
                                    knowledge_id=knowledge_id)
                Workflow.create_workflow(workflow)
                workflow = Workflow.get_workflow_by_owner_name(workflow_name)
                my_workflow_tasks = []
                for dataset_id in dataset_ids:
                    dataset = Dataset.get_dataset_by_id(dataset_id)
                    prompt = Prompt.get_prompt_by_id(experiment.prompt_id)
                    entity_model = Model.get_model_by_id(experiment.entity_extract_model_id)
                    attribute_model = Model.get_model_by_id(experiment.attribute_extract_model_id)
                    relation_model = Model.get_model_by_id(experiment.relation_extract_model_id)

                    for dataset_split in Dataset_Split.get_dataset_splits_by_dataset_id(dataset_id):

                        workflow_task = Workflow_Task(owner=st.session_state.current_username,
                                                      workflow_id=workflow.id,
                                                      experiment_id=experiment_id,
                                                      dataset_id=dataset_id,
                                                      dataset_split_id=dataset_split.id,
                                                      knowledge_id=knowledge_id,
                                                      dataset_split_name=dataset_split.name,
                                                      dataset_split_content=dataset_split.content,
                                                      character=prompt.character,
                                                      entity_model_content=entity_model.content,
                                                      entity_extract=prompt.entity_extract,
                                                      entity_extract_parse=prompt.entity_extract_parse,
                                                      attribute_model_content=attribute_model.content,
                                                      attribute_extract=prompt.attribute_extract,
                                                      attribute_extract_parse=prompt.attribute_extract_parse,
                                                      relation_model_content=relation_model.content,
                                                      relation_extract=prompt.relation_extract,
                                                      relation_extract_parse=prompt.relation_extract_parse)
                        my_workflow_tasks.append(workflow_task)
                Workflow_Task.create_workflow_tasks_batch()
                st.success('工作流创建成功！', icon=':material/done:')
            except Exception as e:
                st.error('工作流创建失败，错误原因：{}！'.format(e), icon=':material/error:')