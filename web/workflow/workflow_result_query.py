import streamlit as st
from web.database.workflow import Workflow
from web.database.workflow_task import Workflow_Task
from web.database.dataset import Dataset


st.header('工作流结果查询')
st.session_state.current_page = 'workflow_result_query_page'

with st.container(border=True):
    my_workflows = []
    for workflow in Workflow.get_workflows_by_owner():
        my_workflows.append('{}: 【{}】'.format(workflow.id, workflow.name))
    workflow_select = st.selectbox('选择工作流', options=my_workflows, key='workflow_select')

    my_workflow_tasks = []
    if workflow_select is not None:
        workflow_id = workflow_select.split(':')[0]
        for workflow_task in Workflow_Task.get_workflow_tasks_by_workflow_id(workflow_id):
            dataset = Dataset.get_dataset_by_id(workflow_task.dataset_id)
            my_workflow_tasks.append('{}: 【{}】'.format(workflow_task.id, workflow_task.dataset_split_name))
    workflow_task_select = st.selectbox('选择工作流任务', options=my_workflow_tasks, key='workflow_task_select')

    if workflow_task_select is not None:
        workflow_task_id = workflow_task_select.split(':')[0]
        workflow_task = Workflow_Task.get_workflow_task_by_id(workflow_task_id)

        st.text('原始数据内容：')
        st.code(workflow_task.dataset_split_content, wrap_lines=True)

        entity_extract_result_code = []
        if workflow_task.entity_extract_result is not None:
            entity_extract_result_code = eval(workflow_task.entity_extract_result)
        st.text('实体抽取结果：{}个实体'.format(len(entity_extract_result_code)))
        st.code(entity_extract_result_code, wrap_lines=True, language="json")

        attribute_extract_result_code = []
        if workflow_task.attribute_extract_result is not None:
            attribute_extract_result_code = eval(workflow_task.attribute_extract_result)
        st.text('属性抽取结果：{}个属性'.format(len(attribute_extract_result_code)))
        st.code(attribute_extract_result_code, wrap_lines=True, language="json")

        relation_extract_result_code = []
        if workflow_task.relation_extract_result is not None:
            relation_extract_result_code = eval(workflow_task.relation_extract_result)
        st.text('关系抽取结果：{}个关系'.format(len(relation_extract_result_code)))
        st.code(relation_extract_result_code, wrap_lines=True, language="json")
