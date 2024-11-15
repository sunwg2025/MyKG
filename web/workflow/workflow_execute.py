import streamlit as st
from web.database.workflow import Workflow
from web.database.workflow_task import Workflow_Task
from web.database.dataset import Dataset
from web.database.knowledge import Knowledge
from web.tools.model import extract_entity_knowledge, extract_attribute_knowledge, extract_relation_knowledge
from web.tools.knowledge import load_knowledge_from_xml, add_knowledge_entity, add_knowledge_attribute
from web.tools.knowledge import add_knowledge_relation
from datetime import datetime
from web.database import session


st.header('工作流执行')
st.session_state.current_page = 'workflow_execute_page'


st.subheader('Step 1：选择工作流', divider=True)
with st.container(border=True):
    my_workflows = []
    for workflow in Workflow.get_workflows_by_owner():
        my_workflows.append('{}: 【{}】'.format(workflow.id, workflow.name))
    workflow_select = st.selectbox('选择工作流', options=my_workflows, key='workflow_select')

    data = []
    if workflow_select is not None:
        workflow_id = workflow_select.split(':')[0]
        workflow = Workflow.get_workflow_by_id(workflow_id)
        workflow_tasks = Workflow_Task.get_workflow_tasks_by_workflow_id(workflow_id)
        for workflow_task in workflow_tasks:
            if_run = True
            if workflow_task.finish_at is not None:
                if_run = False
            dataset = Dataset.get_dataset_by_id(workflow_task.dataset_id)
            data.append({'是否执行': if_run, '任务ID': workflow_task.id, '数据集名': dataset.name,
                         '实体抽取结果': workflow_task.entity_extract_result,
                         '属性抽取结果': workflow_task.attribute_extract_result,
                         '关系抽取结果': workflow_task.relation_extract_result,
                         '任务开始时间': workflow_task.start_at, '任务结束时间': workflow_task.finish_at})

    column_config = {
        '是否执行': st.column_config.CheckboxColumn('是否执行', width='small'),
        '任务ID': st.column_config.NumberColumn('任务ID', width='small'),
        '数据集名': st.column_config.TextColumn('数据集名', width='small'),
        '实体抽取结果': st.column_config.TextColumn('实体抽取结果', width='small', help='点击以查看完整数据'),
        '属性抽取结果': st.column_config.TextColumn('属性抽取结果', width='small', help='点击以查看完整数据'),
        '关系抽取结果': st.column_config.TextColumn('关系抽取结果', width='small', help='点击以查看完整数据'),
        '任务开始时间': st.column_config.DatetimeColumn('任务开始时间', width='small'),
        '任务结束时间': st.column_config.DatetimeColumn('任务结束时间', width='small')
    }
    edited_datas = st.data_editor(data, column_config=column_config, hide_index=False, num_rows="fixed",
                                  use_container_width=True)

st.subheader('Step 2：执行工作流', divider=True)
with st.container(border=True):
    if st.button('执行'):
        error = False
        if workflow_select is None:
            st.error('请选择工作流后在执行！', icon=':material/error:')
            error = True
        if not error:
            task_cnt = 0
            for edited_data in edited_datas:
                if edited_data['是否执行']:
                    task_cnt += 1
            if task_cnt == 0:
                st.error('请选择要执行的任务！', icon=':material/error:')
                error = True
        if not error:
            progress_text = "执行中，请等待..."
            my_bar = st.progress(0, text=progress_text)

            my_bar_progress = 1 / (task_cnt * 4)

            st.text('{}: 任务开始执行...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            index = 1
            for edited_data in edited_datas:
                if not edited_data['是否执行']:
                    continue
                task_start_at = datetime.now()
                dataset_name = edited_data['数据集名']
                workflow_task_id = edited_data['任务ID']
                workflow_task = Workflow_Task.get_workflow_task_by_id(workflow_task_id)

                entity_extract_result = extract_entity_knowledge(dataset_content=workflow_task.dataset_content,
                                                                 model_content=workflow_task.entity_model_content,
                                                                 character=workflow_task.character,
                                                                 extract_prompt=workflow_task.entity_extract,
                                                                 extract_parse=workflow_task.entity_extract_parse)

                my_bar.progress(my_bar_progress * index, text='{}% - 数据集{} : {} 执行完成...'.format(round(index*my_bar_progress*100, 2), dataset_name, '实体抽取'))
                index += 1
                st.text('{}: 数据集[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_name, '实体抽取'))

                attribute_extract_result = extract_attribute_knowledge(dataset_content=workflow_task.dataset_content,
                                                                       model_content=workflow_task.attribute_model_content,
                                                                       entity_content=str(entity_extract_result),
                                                                       character=workflow_task.character,
                                                                       extract_prompt=workflow_task.attribute_extract,
                                                                       extract_parse=workflow_task.attribute_extract_parse)
                my_bar.progress(my_bar_progress * index, text='{}% - 数据集{} : {} 执行完成...'.format(round(index*my_bar_progress*100, 2), dataset_name, '属性抽取'))
                index += 1
                st.text('{}: 数据集[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_name, '属性抽取'))

                relation_extract_result = extract_relation_knowledge(dataset_content=workflow_task.dataset_content,
                                                                     model_content=workflow_task.relation_model_content,
                                                                     entity_content=str(entity_extract_result),
                                                                     character=workflow_task.character,
                                                                     extract_prompt=workflow_task.relation_extract,
                                                                     extract_parse=workflow_task.relation_extract_parse)
                my_bar.progress(my_bar_progress * index, text='{}% - 数据集{} : {} 执行完成...'.format(round(index*my_bar_progress*100, 2), dataset_name, '关系抽取'))
                index += 1
                st.text('{}: 数据集[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_name, '关系抽取'))

                knowledge = Knowledge.get_knowledge_by_id(workflow.knowledge_id)
                graph = load_knowledge_from_xml(knowledge.rdf_xml)
                for entity_data in entity_extract_result:
                    add_knowledge_entity(graph, entity_data)

                for attribute_data in attribute_extract_result:
                    try:
                        entity = attribute_data[0]
                        attribute_type = attribute_data[1]
                        attribute_value = attribute_data[2]
                        add_knowledge_attribute(graph, entity, attribute_type, attribute_value)
                    except Exception as e:
                        continue

                for relation_data in relation_extract_result:
                    try:
                        entity1 = relation_data[0]
                        relation = relation_data[1]
                        entity2 = relation_data[2]
                        add_knowledge_relation(graph, entity1, relation, entity2)
                    except Exception as e:
                        continue
                try:
                    rdf_xml = graph.serialize(format='xml')
                    knowledge.rdf_xml = rdf_xml
                    knowledge.update_at = datetime.now()
                    session.commit()
                    graph.close()
                except Exception as e:
                    session.rollback()
                    st.error('知识库更新失败，错误原因：{}！'.format(e), icon=':material/error:')

                try:
                    workflow_task.entity_extract_result = str(entity_extract_result)
                    workflow_task.attribute_extract_result = str(attribute_extract_result)
                    workflow_task.relation_extract_result = str(relation_extract_result)
                    workflow_task.start_at = task_start_at
                    workflow_task.finish_at = datetime.now()
                    session.commit()
                except Exception as e:
                    session.rollback()
                    st.error('工作流任务更新失败，错误原因：{}！'.format(e), icon=':material/error:')
                my_bar.progress(my_bar_progress * index, text='{}% - 数据集{} : {} 执行完成...'.format(round(index*my_bar_progress*100, 2), dataset_name, '知识库更新'))
                index += 1
                st.text('{}: 数据集[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_name, '知识库更新'))


st.subheader('Step 3：查看执行结果', divider=True)
with st.container(border=True):
    my_workflow_tasks = []
    if workflow_select is not None:
        workflow_id = workflow_select.split(':')[0]
        for workflow_task in Workflow_Task.get_workflow_tasks_by_workflow_id(workflow_id):
            dataset = Dataset.get_dataset_by_id(workflow_task.dataset_id)
            my_workflow_tasks.append('{}: 【{}】'.format(workflow_task.id, dataset.name))
    workflow_task_select = st.selectbox('选择工作流任务', options=my_workflow_tasks, key='workflow_task_select')

    if workflow_task_select is not None:
        workflow_task_id = workflow_task_select.split(':')[0]
        workflow_task = Workflow_Task.get_workflow_task_by_id(workflow_task_id)

        st.text('实体抽取结果：')
        entity_extract_result_code = []
        if workflow_task.entity_extract_result is not None:
            entity_extract_result_code = workflow_task.entity_extract_result
        st.code(entity_extract_result_code, wrap_lines=True, language="json")

        st.text('属性抽取结果：')
        attribute_extract_result_code = []
        if workflow_task.attribute_extract_result is not None:
            attribute_extract_result_code = workflow_task.attribute_extract_result
        st.code(attribute_extract_result_code, wrap_lines=True, language="json")

        st.text('关系抽取结果：')
        relation_extract_result_code = []
        if workflow_task.relation_extract_result is not None:
            relation_extract_result_code = workflow_task.relation_extract_result
        st.code(relation_extract_result_code, wrap_lines=True, language="json")