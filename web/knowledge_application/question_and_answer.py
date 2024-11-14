import streamlit as st
from web.database.model import Model
from web.tools.model import analyze_content_entities, analyze_knowledges_choose, generate_knowledges_answer
from web.database.knowledge import Knowledge
from web.tools.knowledge import load_knowledge_from_xml
from web.tools.knowledge import get_entity_attribute_knowledge, get_entity_relation_knowledge
from web.tools.knowledge import get_knowledge_stats

st.header('知识问答')
st.session_state.current_page = 'question_and_answer_page'

with st.container(border=True):
    my_knowledges = []
    for knowledge in Knowledge.get_knowledges_by_owner():
        my_knowledges.append('{}: 【{}】 【{}】'.format(knowledge.id, knowledge.catalog, knowledge.name))
    knowledge_select = st.selectbox('选择知识库', options=my_knowledges)

    if knowledge_select is not None:
        knowledge_id = knowledge_select.split(':')[0]
        knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
        entities_online_cnt, attributes_online_cnt, relations_online_cnt = get_knowledge_stats(knowledge.rdf_xml_online)
        st.text('知识库-生产：')
        st.text('实体个数：{}'.format(entities_online_cnt))
        st.text('属性个数：{}'.format(attributes_online_cnt))
        st.text('关系个数：{}'.format(relations_online_cnt))
        st.text('更新时间：{}'.format(knowledge.update_at_online))

    question_text = st.text_area('请输入问题', height=120, key='question_text')
    if st.button('提交'):
        error = False
        if knowledge_select is None:
            st.error('知识库不能为空，请重新输入！', icon=':material/error:')
            error = True
        if question_text.strip() == '' and not error:
            st.error('问题不能为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            default_model = Model.get_default_model_by_owner()
            if default_model is None:
                st.error('用户未设置默认模型，请设置完成后在执行！', icon=':material/error:')
                error = True
            else:
                entities_result = analyze_content_entities(question_text, default_model.content)
                st.text('实体识别结果：{}'.format(entities_result))
                knowledge_id = knowledge_select.split(':')[0]
                knowledge = Knowledge.get_knowledge_by_id(knowledge_id)
                graph = load_knowledge_from_xml(knowledge.rdf_xml_online)
                knowledge_details = []
                for entity in entities_result:
                    attributes = get_entity_attribute_knowledge(graph, entity)
                    for attribute in attributes:
                        knowledge_details.append(attribute)
                for entity in entities_result:
                    relations = get_entity_relation_knowledge(graph, entity)
                    for relation in relations:
                        knowledge_details.append(relation)

                st.text('备选知识明细：{}'.format(knowledge_details))
                knowledge_chooses = analyze_knowledges_choose(str(knowledge_details), question_text, default_model.content)
                st.text('知识选择结果：{}'.format(knowledge_chooses))

                if len(knowledge_chooses) == 0:
                    st.error('在知识库中未找到与用户问题相关的知识，无法回答问题！', icon=':material/error:')
                else:
                    final_answer = generate_knowledges_answer(str(knowledge_chooses), question_text, default_model.content)
                    st.text_area('知识生成结果：', value=final_answer, height=360)



