import streamlit as st
from web.database.dataset import Dataset
from web.database import session

st.header('输入数据集创建')

st.session_state.current_page = 'input_dataset_page'

with st.form('submit'):
    dataset_content = st.text_area('数据内容', height=360, max_chars=4096, key='dataset_content')
    tags = st.text_input('数据标签', max_chars=64, help='数据内容的关键词，逗号分隔', key='tags')

    catalog_name = st.text_input('数据类目', key='catalog_name')
    dataset_name = st.text_input('数据集名', key='dataset_name')

    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if Dataset.get_dataset_by_owner_with_name(dataset_name) is not None:
            st.error('用户下同名数据集已存在，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                dataset = Dataset(catalog=catalog_name,
                                  name=dataset_name,
                                  owner=st.session_state.current_username,
                                  channel='input',
                                  source='',
                                  content=dataset_content,
                                  tags=tags)
                session.add(dataset)
                session.commit()
                st.success('数据集创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('数据集创建失败，错误原因：{}！'.format(e), icon=':material/error:')

