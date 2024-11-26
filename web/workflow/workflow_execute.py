import streamlit as st
from web.database.workflow import Workflow
from web.database.workflow_task import Workflow_Task
from web.database.dataset import Dataset
from web.database.knowledge import Knowledge
from web.tools.model import extract_entity_knowledge, extract_attribute_knowledge, extract_relation_knowledge
from web.tools.knowledge import load_knowledge_from_xml, add_knowledge_entity, add_knowledge_attribute
from web.tools.knowledge import add_knowledge_relation
from datetime import datetime

st.header('工作流执行-前台')
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
            entities_cnt = 0
            if workflow_task.entity_extract_result is not None:
                entities_cnt = len(eval(workflow_task.entity_extract_result))
            attributes_cnt = 0
            if workflow_task.attribute_extract_result is not None:
                attributes_cnt = len(eval(workflow_task.attribute_extract_result))
            relations_cnt = 0
            if workflow_task.relation_extract_result is not None:
                relations_cnt = len(eval(workflow_task.relation_extract_result))
            extract_results = 'EAR：{}-{}-{}'.format(entities_cnt, attributes_cnt, relations_cnt)
            data.append({'执行': if_run, 'ID': workflow_task.id,
                         '数据分片': workflow_task.dataset_split_name,
                         '抽取结果': extract_results,
                         '抽取时间': workflow_task.finish_at})

    column_config = {
        '执行': st.column_config.CheckboxColumn('执行', width='small'),
        'ID': st.column_config.NumberColumn('ID', width='small'),
        '数据分片': st.column_config.TextColumn('数据分片', width='medium'),
        '抽取结果': st.column_config.TextColumn('抽取结果', width='medium'),
        '抽取时间': st.column_config.DatetimeColumn('抽取时间', width='medium')
    }
    edited_datas = st.data_editor(data, column_config=column_config, hide_index=True, num_rows="fixed",
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
                if edited_data['执行']:
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
                if not edited_data['执行']:
                    continue
                task_start_at = datetime.now()
                dataset_split_name = edited_data['数据分片']
                workflow_task_id = edited_data['ID']
                Workflow_Task.clear_workflow_task_by_id(workflow_task_id)
                workflow_task = Workflow_Task.get_workflow_task_by_id(workflow_task_id)

                entity_extract_result = extract_entity_knowledge(dataset_content=workflow_task.dataset_split_content,
                                                                 model_content=workflow_task.entity_model_content,
                                                                 character=workflow_task.character,
                                                                 extract_prompt=workflow_task.entity_extract,
                                                                 extract_parse=workflow_task.entity_extract_parse)

                my_bar.progress(my_bar_progress * index,
                                text='{}% - 数据分片{} : {} 执行完成...'.format(round(index * my_bar_progress * 100, 2),
                                                                        dataset_split_name, '实体抽取'))
                index += 1
                st.text(
                    '{}: 数据分片[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_split_name,
                                                       '实体抽取'))

                attribute_extract_result = extract_attribute_knowledge(
                    dataset_content=workflow_task.dataset_split_content,
                    model_content=workflow_task.attribute_model_content,
                    entity_content=str(entity_extract_result),
                    character=workflow_task.character,
                    extract_prompt=workflow_task.attribute_extract,
                    extract_parse=workflow_task.attribute_extract_parse)
                my_bar.progress(my_bar_progress * index,
                                text='{}% - 数据分片{} : {} 执行完成...'.format(round(index * my_bar_progress * 100, 2),
                                                                        dataset_split_name, '属性抽取'))
                index += 1
                st.text(
                    '{}: 数据分片[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_split_name,
                                                       '属性抽取'))

                relation_extract_result = extract_relation_knowledge(
                    dataset_content=workflow_task.dataset_split_content,
                    model_content=workflow_task.relation_model_content,
                    entity_content=str(entity_extract_result),
                    character=workflow_task.character,
                    extract_prompt=workflow_task.relation_extract,
                    extract_parse=workflow_task.relation_extract_parse)
                my_bar.progress(my_bar_progress * index,
                                text='{}% - 数据分片{} : {} 执行完成...'.format(round(index * my_bar_progress * 100, 2),
                                                                        dataset_split_name, '关系抽取'))
                index += 1
                st.text(
                    '{}: 数据分片[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_split_name,
                                                       '关系抽取'))

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
                    knowledge.update_knowledge_rdf_xml(rdf_xml)
                    graph.close()
                except Exception as e:
                    st.error('知识库更新失败，错误原因：{}！'.format(e), icon=':material/error:')

                try:
                    workflow_task = Workflow_Task.get_workflow_task_by_id(workflow_task_id)
                    workflow_task.update_workflow_task(str(entity_extract_result), str(attribute_extract_result),
                                                       str(relation_extract_result), task_start_at)
                except Exception as e:
                    st.error('工作流任务更新失败，错误原因：{}！'.format(e), icon=':material/error:')
                my_bar.progress(my_bar_progress * index,
                                text='{}% - 数据分片{} : {} 执行完成...'.format(round(index * my_bar_progress * 100, 2),
                                                                        dataset_split_name, '知识库更新'))
                index += 1
                st.text(
                    '{}: 数据分片[{}] - {} 执行完成...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), dataset_split_name,
                                                       '知识库更新'))
