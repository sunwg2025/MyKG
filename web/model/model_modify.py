import streamlit as st
from web.database.model import Model
from web.tools.model import check_model_config

st.header('模型变更')
st.session_state.current_page = 'model_modify_page'

my_models = []
for model in Model.get_models_by_owner():
    my_models.append('{}: 【{}】'.format(model.id, model.name))
model_select = st.selectbox('选择模型', options=my_models)

model_content_value = ''
model_name_value = ''
is_default_value = False
if model_select is not None:
    model_id = model_select.split(':')[0]
    model = Model.get_model_by_id(model_id)
    model_content_value = model.content
    model_name_value = model.name
    is_default_value = model.is_default

with st.form("submit"):
    model_name = st.text_input('模型名', value=model_name_value, help='6-64个字符，可使用字母、数字、下划线，需以字母开头')
    model_content = st.text_area('模型配置', value=model_content_value, height=420, max_chars=4096)
    is_default = st.toggle("默认", value=is_default_value, key='is_default')

    delete = st.toggle("删除")
    submit_button = st.form_submit_button('提交')
    if submit_button:
        model_id = model_select.split(':')[0]
        if delete:
            try:
                Model.delete_model_by_id(model_id)
                st.success('模型配置删除成功！', icon=':material/done:')
            except Exception as e:
                st.error('模型配置删除失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            error = False
            same_model = Model.get_model_by_owner_with_name(model_name)
            if same_model:
                if str(same_model.id) != str(model_id):
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
                    new = Model(name=model_name, content=model_content, is_default=is_default)
                    model.update_model_columns(new)
                    st.success('模型更新成功！', icon=':material/done:')
                except Exception as e:
                    st.error('模型更新失败，错误原因：{}！'.format(e), icon=':material/error:')

