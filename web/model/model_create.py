import streamlit as st
from web.database.model_template import Model_Template
from web.database.model import Model
from web.database import session
from web.tools.model import check_model_config

st.header('模型创建')
st.session_state.current_page = 'model_create_page'

model_templates = []
for template in Model_Template.get_all_templates():
    model_templates.append('{}: 【{}】'.format(template.id, template.name))
template_select = st.selectbox('选择模型模板', options=model_templates)

template_model_content = ''
if template_select is not None:
    template_id = template_select.split(':')[0]
    model_template = Model_Template.get_template_by_id(template_id)
    template_model_content = model_template.content

with st.form('submit'):
    model_content = st.text_area('模型配置', value=template_model_content, height=420, max_chars=4096)
    model_name = st.text_input('模型名', key='model_name')
    is_default = st.toggle('默认', key='is_default')

    submit_button = st.form_submit_button('提交')

    if submit_button:
        error = False
        if Model.get_model_by_owner_with_name(model_name) is not None:
            st.error('用户下已有同名模型，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                check_model_config(model_content)
            except Exception as e:
                st.error('模型配置测试失败，错误原因：{}！'.format(e), icon=':material/error:')
                error = True
        if not error:
            try:
                if is_default:
                    Model.clear_default_model_by_owner()
                model = Model(name=model_name,
                              owner=st.session_state.current_username,
                              content=model_content,
                              is_default=is_default)
                session.add(model)
                session.commit()
                st.success('模型创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('模型创建失败，错误原因：{}！'.format(e), icon=':material/error:')
