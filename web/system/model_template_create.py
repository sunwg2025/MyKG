import streamlit as st
from web.database.model_template import Model_Template
from web.database import session

st.header('模型模版创建')
st.session_state.current_page = 'model_template_create_page'

with st.form('submit'):
    template_name = st.text_input('模板名', key='template_name')
    template_content = st.text_area('模板配置', height=480, max_chars=4096, key='template_content')

    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if Model_Template.get_template_by_name(template_name) is not None:
            st.error('同名模型模板已存在，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                template = Model_Template(name=template_name,
                                          content=template_content)
                session.add(template)
                session.commit()
                st.success('模板文件创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('模板文件创建失败，错误原因：{}！'.format(e), icon=':material/error:')
