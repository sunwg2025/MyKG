import streamlit as st
from web.database import session
from web.database.dataset import Dataset

st.header("数据集变更")
st.session_state.current_page = 'dataset_modify_page'

my_datasets = []
for dataset in Dataset.get_datasets_by_owner():
    my_datasets.append('{}: 【{}】 【{}】'.format(dataset.id, dataset.catalog, dataset.name))
dataset_select = st.selectbox('选择数据集', options=my_datasets)

dataset_name = ''
catalog_name = ''
content = ''
tags = ''

if dataset_select is not None:
    dataset_id = dataset_select.split(':')[0]
    dataset = Dataset.get_dataset_by_id(dataset_id)
    dataset_name = dataset.name
    catalog_name = dataset.catalog
    content = dataset.content
    tags = dataset.tags

with st.form('submit'):
    content = st.text_area('数据内容', value=content, height=360, max_chars=4096)
    tags = st.text_input('数据标签', value=tags, max_chars=64, help='数据内容的关键词，逗号分隔')

    dataset_name = st.text_input('数据集名', value=dataset_name, help='6-64个字符，可使用字母、数字、下划线，需以字母开头')
    catalog_name = st.text_input('数据类目', value=catalog_name, help='6-64个字符，可使用字母、数字、下划线，需以字母开头')
    delete = st.toggle('删除')
    submit_button = st.form_submit_button('提交')
    if submit_button:
        dataset_id = dataset_select.split(':')[0]
        if delete:
            try:
                Dataset.delete_dataset_by_id(dataset_id)
                st.success('数据集删除成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('数据集删除失败，错误原因：{}！'.format(e), icon=':material/error:')
        else:
            error = False
            if str(Dataset.get_dataset_by_owner_with_name(dataset_name).id) != str(dataset_id):
                st.error('用户下已有同名数据集，请重新输入！', icon=':material/error:')
                error = True
            if not error:
                try:
                    dataset = Dataset.get_dataset_by_id(dataset_id)
                    new = Dataset(catalog=catalog_name,
                                  name=dataset_name,
                                  content=content,
                                  tags=tags)
                    dataset.update_dataset_columns(new)
                    st.success('数据集更新成功！', icon=':material/done:')
                except Exception as e:
                    session.rollback()
                    st.error('数据集更新失败，错误原因：{}！'.format(e), icon=':material/error:')
