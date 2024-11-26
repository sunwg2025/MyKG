import streamlit as st
from web.database.model_template import Model_Template

st.header('模型模板管理')
st.session_state.current_page = 'model_template_modify_page'

my_model_templates = []
for model_template in Model_Template.get_all_templates():
    my_model_templates.append('{}: 【{}】'.format(model_template.id, model_template.name))
model_templates_select = st.selectbox('选择模型模板', options=my_model_templates)

template_name_value = ''
template_content_value = ''

if model_templates_select is not None:
    model_template_id = model_templates_select.split(':')[0]
    model_template = Model_Template.get_template_by_id(model_template_id)
    template_name_value = model_template.name
    template_content_value = model_template.content

with st.form("submit"):
    template_name = st.text_input('模板名', value=template_name_value, key='template_name')
    template_content = st.text_area('模板配置', value=template_content_value, height=240, max_chars=4096)
    delete = st.toggle('删除')

    submit_button = st.form_submit_button('提交')
    if submit_button:
        model_template_id = model_templates_select.split(':')[0]
        model_template = Model_Template.get_template_by_id(model_template_id)
        if delete:
            try:
                Model_Template.delete_model_template_by_id(model_template_id)
                st.success('模型模板删除成功！', icon=':material/done:')
            except Exception as e:
                st.error('模型模板删除失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            try:
                new = Model_Template(name=template_name, content=template_content)
                model_template.update_model_template_columns(new)
                st.success('模型模板更新成功！', icon=':material/done:')
            except Exception as e:
                st.error('模型模板更新失败，错误原因：{}！'.format(e), icon=':material/error:')

