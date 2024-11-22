import streamlit as st
from web.database.system_prompt import System_Prompt
from web.database import session

st.header('工具提示词变更')
st.session_state.current_page = 'system_prompt_modify_page'

st.subheader('关键词识别', divider=True)
with st.form('tags'):
    system_prompt_tags = System_Prompt.get_system_prompt_by_name('Tags_Analyze')
    if 'tags_analyze' not in st.session_state:
        if system_prompt_tags:
            st.session_state['tags_analyze'] = system_prompt_tags.content
            st.session_state['tags_result'] = system_prompt_tags.result
    tags_analyze = st.text_area('关键词分析', height=240, max_chars=4096, key='tags_analyze')
    tags_result = st.text_area('关键词结果', height=120, max_chars=4096, key='tags_result')

    tags_analyze_submit = st.form_submit_button('提交')
    if tags_analyze_submit:
        system_prompt = System_Prompt.get_system_prompt_by_name('Tags_Analyze')
        if system_prompt is not None:
            try:
                System_Prompt.update_system_prompt_by_name('Tags_Analyze', tags_analyze, tags_result)
                st.success('工具提示词更新成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                system_prompt = System_Prompt(name='Tags_Analyze', content=tags_analyze, result=tags_result)
                session.add(system_prompt)
                session.commit()
                st.success('工具提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')


st.subheader('文本摘要生成', divider=True)
with st.form('summary'):
    system_prompt_summary = System_Prompt.get_system_prompt_by_name('Summary_Analyze')
    if 'summary_analyze' not in st.session_state:
        if system_prompt_summary:
            st.session_state['summary_analyze'] = system_prompt_summary.content
            st.session_state['summary_result'] = system_prompt_summary.result
    summary_analyze = st.text_area('文本摘要分析', height=240, max_chars=4096, key='summary_analyze')
    summary_result = st.text_area('摘要结果', height=120, max_chars=4096, key='summary_result')

    summary_analyze_submit = st.form_submit_button('提交')
    if summary_analyze_submit:
        system_prompt = System_Prompt.get_system_prompt_by_name('Summary_Analyze')
        if system_prompt is not None:
            try:
                System_Prompt.update_system_prompt_by_name('Summary_Analyze', summary_analyze, summary_result)
                st.success('工具提示词更新成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                system_prompt = System_Prompt(name='Summary_Analyze', content=summary_analyze, result=summary_result)
                session.add(system_prompt)
                session.commit()
                st.success('工具提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')


st.subheader('实体识别', divider=True)
with st.form('entities'):
    system_prompt_entities = System_Prompt.get_system_prompt_by_name('Entities_Analyze')
    if 'entities_analyze' not in st.session_state:
        if system_prompt_entities:
            st.session_state['entities_analyze'] = system_prompt_entities.content
            st.session_state['entities_result'] = system_prompt_entities.result
    entities_analyze = st.text_area('实体分析', height=240, max_chars=4096, key='entities_analyze')
    entities_result = st.text_area('实体结果', height=120, max_chars=4096, key='entities_result')

    entities_analyze_submit = st.form_submit_button('提交')
    if entities_analyze_submit:
        system_prompt = System_Prompt.get_system_prompt_by_name('Entities_Analyze')
        if system_prompt is not None:
            try:
                System_Prompt.update_system_prompt_by_name('Entities_Analyze', entities_analyze, entities_result)
                st.success('工具提示词更新成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                system_prompt = System_Prompt(name='Entities_Analyze', content=entities_analyze, result=entities_result)
                session.add(system_prompt)
                session.commit()
                st.success('工具提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')


st.subheader('知识选择', divider=True)
with st.form('knowledges'):
    system_prompt_knowledges = System_Prompt.get_system_prompt_by_name('Knowledges_Choose')
    if 'knowledges_choose' not in st.session_state:
        if system_prompt_knowledges:
            st.session_state['knowledges_choose'] = system_prompt_knowledges.content
            st.session_state['knowledges_result'] = system_prompt_knowledges.result
    knowledges_choose = st.text_area('知识选择', height=240, max_chars=4096, key='knowledges_choose')
    knowledges_result = st.text_area('选择结果', height=120, max_chars=4096, key='knowledges_result')

    knowledges_choose_submit = st.form_submit_button('提交')
    if knowledges_choose_submit:
        system_prompt = System_Prompt.get_system_prompt_by_name('Knowledges_Choose')
        if system_prompt is not None:
            try:
                System_Prompt.update_system_prompt_by_name('Knowledges_Choose', knowledges_choose, knowledges_result)
                st.success('工具提示词更新成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                system_prompt = System_Prompt(name='Knowledges_Choose', content=knowledges_choose, result=knowledges_result)
                session.add(system_prompt)
                session.commit()
                st.success('工具提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')


st.subheader('知识回答', divider=True)
with st.form('answer'):
    system_prompt_answers = System_Prompt.get_system_prompt_by_name('Knowledges_Answer')
    if 'knowledges_answer' not in st.session_state:
        if system_prompt_answers:
            st.session_state['knowledges_answer'] = system_prompt_answers.content
            st.session_state['answers_result'] = system_prompt_answers.result
    knowledges_answer = st.text_area('知识选择', height=240, max_chars=4096, key='knowledges_answer')
    answers_result = st.text_area('选择结果', height=120, max_chars=4096, key='answers_result')

    knowledges_answer_submit = st.form_submit_button('提交')
    if knowledges_answer_submit:
        system_prompt = System_Prompt.get_system_prompt_by_name('Knowledges_Answer')
        if system_prompt is not None:
            try:
                System_Prompt.update_system_prompt_by_name('Knowledges_Answer', knowledges_answer, answers_result)
                st.success('工具提示词更新成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词更新失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                system_prompt = System_Prompt(name='Knowledges_Answer', content=knowledges_answer, result=answers_result)
                session.add(system_prompt)
                session.commit()
                st.success('工具提示词创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('工具提示词创建失败，错误原因：{}！'.format(e), icon=':material/error:')