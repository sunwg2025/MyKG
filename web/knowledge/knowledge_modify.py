import streamlit as st
from web.database.knowledge import Knowledge
from web.tools.knowledge import load_knowledge_from_xml, get_all_entity_knowledge
from web.tools.knowledge import get_all_attribute_knowledge, get_all_relation_knowledge
from web.tools.knowledge import remove_knowledge_attribute, remove_knowledge_relation, remove_knowledge_entity
from web.tools.knowledge import add_knowledge_relation, add_knowledge_attribute, add_knowledge_entity
import graphviz
from datetime import datetime

st.header('知识库变更')
st.session_state.current_page = 'knowledge_modify_page'

entities = []
attributes = []
relations = []

st.subheader('Step 1：选择知识库', divider=True)
with st.container(border=True):
    my_knowledges = []
    for knowledge in Knowledge.get_knowledges_by_owner():
        my_knowledges.append('{}: 【{}】'.format(knowledge.id, knowledge.name))
    knowledge_select = st.selectbox('选择知识库', options=my_knowledges)

    if knowledge_select is not None:
        knowledge_id = knowledge_select.split(':')[0]
        knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
        graph = load_knowledge_from_xml(knowledge.rdf_xml)
        entities = get_all_entity_knowledge(graph)
        attributes = get_all_attribute_knowledge(graph)
        relations = get_all_relation_knowledge(graph)

        entities_count_text = st.text('实体个数：{}'.format(len(entities)))
        attributes_count_text = st.text('属性个数：{}'.format(len(attributes)))
        relations_count_text = st.text('关系个数：{}'.format(len(relations)))

        @st.dialog("知识库实体关系图")
        def vote(relations):
            graph_chart = graphviz.Digraph()
            graph_chart.graph_attr['color'] = 'blue'
            graph_chart.graph_attr['rankdir'] = 'LR'

            # 设置节点属性
            graph_chart.node_attr['shape'] = 'box'
            graph_chart.node_attr['style'] = 'filled'
            graph_chart.node_attr['fillcolor'] = 'lightgrey'

            # 设置边属性
            graph_chart.edge_attr['color'] = 'red'
            graph_chart.edge_attr['style'] = 'dashed'

            for relation in relations:
                entity_node1 = 'E-{}'.format(relation['实体1'])
                relation_type = 'R-{}'.format(relation['关系'])
                entity_node2 = 'E-{}'.format(relation['实体2'])
                graph_chart.edge(tail_name=entity_node1, head_name=entity_node2, label=relation_type)
            st.graphviz_chart(graph_chart, use_container_width=True)
            if st.button("Submit"):
                st.rerun()
        if st.button('显示关系图'):
            vote(relations)

st.subheader('Step 2：知识条目变更', divider=True)
with st.container(border=True):
    entity_attributes = {}
    entity_relations = {}
    for entity in entities:
        entity_attributes[entity] = []
        entity_relations[entity] = []
    for attribute in attributes:
        entity_node = attribute['实体']
        entity_attributes[entity_node].append(attribute)
    for relation in relations:
        entity_node1 = relation['实体1']
        entity_node2 = relation['实体2']
        entity_relations[entity_node1].append(relation)
        entity_relations[entity_node2].append(relation)
    entity_options = []
    for entity in entities:
        attributes_cnt = len(entity_attributes[entity])
        relations_cnt = len(entity_relations[entity])
        entity_options.append('{}: 属性数{} 关系数{}'.format(entity, attributes_cnt, relations_cnt))
    entity_select = st.selectbox('选择知识实体', options=entity_options, key='entity_select')

    attribute_data = [{'实体': '', '属性': '', '属性值': ''}]
    if entity_select is not None:
        entity = entity_select.split(':')[0]
        if len(entity_attributes[entity]) > 0:
            attribute_data = []
        for attribute in entity_attributes[entity]:
            attribute_type = attribute['属性']
            attribute_value = attribute['属性值']
            attribute_data.append({'实体': entity, '属性': attribute_type, '属性值': attribute_value})
    column_config = {
        '实体': st.column_config.TextColumn('实体', width='small'),
        '属性': st.column_config.TextColumn('属性', width='medium'),
        '属性值': st.column_config.TextColumn('属性值', width="large", help='点击以查看完整数据')
    }
    st.text('实体属性')
    attribute_datas = st.data_editor(attribute_data, column_config=column_config, hide_index=False, num_rows="dynamic",
                                     use_container_width=True)

    relation_data = [{'实体1': '', '关系': '', '实体2': ''}]
    if entity_select is not None:
        entity = entity_select.split(':')[0]
        if len(entity_relations[entity]) > 0:
            relation_data = []
        for relation in entity_relations[entity]:
            entity1 = relation['实体1']
            relation_type = relation['关系']
            entity2 = relation['实体2']
            relation_data.append({'实体1': entity1, '关系': relation_type, '实体2': entity2})
    column_config = {
        '实体1': st.column_config.TextColumn('实体1', width='small'),
        '关系': st.column_config.TextColumn('关系', width='small'),
        '实体2': st.column_config.TextColumn('实体2', width="small")
    }
    st.text('实体关系')
    relation_datas = st.data_editor(relation_data, column_config=column_config, hide_index=False, num_rows="dynamic",
                                    use_container_width=True)

    delete = st.toggle('删除')
    if st.button('提交'):
        error = False
        if entity_select is None:
            st.error('知识实体不能为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            for relation in entity_relations[entity]:
                entity1 = relation['实体1']
                relation_type = relation['关系']
                entity2 = relation['实体2']
                remove_knowledge_relation(graph, entity1, relation_type, entity2)
            for attribute in entity_attributes[entity]:
                attribute_type = attribute['属性']
                attribute_value = attribute['属性值']
                remove_knowledge_attribute(graph, entity, attribute_type, attribute_value)
            remove_knowledge_entity(graph, entity)
            if not delete:
                for tmp_attribute in attribute_datas:
                    entity = tmp_attribute['实体']
                    attribute_type = tmp_attribute['属性']
                    attribute_value = tmp_attribute['属性值']
                    if entity != '' and attribute_type != '' and attribute_value != '':
                        add_knowledge_attribute(graph, entity, attribute_type, attribute_value)
                for tmp_relation in relation_datas:
                    entity1 = tmp_relation['实体1']
                    relation_type = tmp_relation['关系']
                    entity2 = tmp_relation['实体2']
                    if entity1 != '' and relation_type != '' and entity2 != '':
                        add_knowledge_relation(graph, entity1, relation_type, entity2)
                add_knowledge_entity(graph, entity)
            try:
                rdf_xml = graph.serialize(format='xml')
                knowledge.update_knowledge_rdf_xml(rdf_xml)
                graph.close()
                st.success('知识库更新成功！', icon=':material/done:')
            except Exception as e:
                st.error('知识库更新失败，错误原因：{}！'.format(e), icon=':material/error:')