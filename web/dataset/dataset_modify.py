import streamlit as st
from web.database import session
from web.database.dataset import Dataset
from web.database.dataset_split import Dataset_Split

st.header("数据集变更")
st.session_state.current_page = 'dataset_modify_page'

my_datasets = []
for dataset in Dataset.get_datasets_by_owner():
    my_datasets.append('{}: 类目【{}】 数据集【{}】 分片数【{}】'.format(dataset.id, dataset.catalog, dataset.name,
                                                           dataset.split_count))
dataset_select = st.selectbox('选择数据集', options=my_datasets)

dataset_name = ''
catalog_name = ''
tags = ''
dataset_splits = []

if dataset_select is not None:
    dataset_id = dataset_select.split(':')[0]
    dataset = Dataset.get_dataset_by_id(dataset_id)
    dataset_name = dataset.name
    catalog_name = dataset.catalog
    tags = dataset.tags
    for dataset_split in Dataset_Split.get_dataset_splits_by_dataset_id(dataset_id):
        dataset_splits.append('{}: 数据分片【{}】 字符数【{}】'.format(dataset_split.id, dataset_split.name,
                                                            dataset_split.total_size))

    with st.container(border=True):
        dataset_split_select = st.selectbox('数据内容', options=dataset_splits)
        if dataset_split_select is not None:
            dataset_split_id = dataset_split_select.split(':')[0]
            dataset_split = Dataset_Split.get_dataset_splits_by_id(dataset_split_id)
            dataset_split_content = st.text_area('数据内容', value=dataset_split.content, label_visibility='collapsed',
                                                 disabled=True, height=360)

with st.form('submit'):
    tags = st.text_input('数据标签', value=tags, max_chars=64, help='数据内容的关键词，逗号分隔')

    dataset_name = st.text_input('数据集名', value=dataset_name)
    catalog_name = st.text_input('数据类目', value=catalog_name)


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
