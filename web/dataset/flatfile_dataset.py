import streamlit as st
from web.database.dataset import Dataset
from web.database.model import Model
from web.database import session
from web.tools.model import analyze_content_tags
from io import StringIO

st.header('文本数据集创建')

if 'file_contents_result' not in st.session_state:
    st.session_state.file_contents_result = []

current_page = 'flatfile_dataset_page'
if st.session_state.current_page != current_page:
    st.session_state.file_contents_result = []
st.session_state.current_page = current_page


type = st.radio('选择创建类型', ['单文件', '多文件'], horizontal=True)
if type == '单文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.form('single_uploader'):
        uploaded_file = st.file_uploader('选择单个文件', accept_multiple_files=False)
        tags_analyze = st.toggle('提取标签', help='调用大模型提取文本标签')
        readfile_button = st.form_submit_button('读取')
        if readfile_button:
            bytes_data = ''
            tags_input = ''
            if uploaded_file is not None:
                bytes_data = StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue()
                if tags_analyze:
                    default_model = Model.get_default_model_by_owner()
                    if default_model is None:
                        st.error('用户未设置默认模型，请设置完成后在执行！', icon=':material/error:')
                    else:
                        tags_result = analyze_content_tags(bytes_data, default_model.content)
                        tags_input = str(tags_result).replace('[', '').replace(']', '')

                st.session_state['dataset_content'] = bytes_data
                st.session_state['tags_input'] = tags_input

    st.subheader('Step 2：创建数据集', divider=True)
    with st.form('single_submit'):
        dataset_content = st.text_area('数据内容', height=360, max_chars=4096, key='dataset_content')
        tags_input = st.text_input('数据标签', max_chars=64, help='数据内容的关键词，逗号分隔', key='tags_input')

        catalog_name = st.text_input('数据类目', help='6-64个字符，可使用字母、数字、下划线，需以字母开头', key='catalog_name')
        dataset_name = st.text_input('数据集名', help='6-64个字符，可使用字母、数字、下划线，需以字母开头', key='dataset_name')

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
                                      channel='flatfile',
                                      source=uploaded_file.name,
                                      content=dataset_content,
                                      tags=tags_input)
                    session.add(dataset)
                    session.commit()
                    st.success('数据集创建成功！', icon=':material/done:')
                except Exception as e:
                    session.rollback()
                    st.error('数据集创建失败，错误原因：{}！'.format(e), icon=':material/error:')
else:
    data = []
    st.subheader('Step 1：选择文件', divider=True)
    with st.form('multiple_uploader'):
        uploaded_files = st.file_uploader('选择多个文件', accept_multiple_files=True)
        tags_analyze = st.toggle('提取标签', help='调用大模型提取文本标签')
        readfile_button = st.form_submit_button('读取')
        if readfile_button:
            for uploaded_file in uploaded_files:
                bytes_data = StringIO(uploaded_file.getvalue().decode('utf-8')).getvalue()
                file_name = uploaded_file.name
                dataset_name = '请输入'
                if tags_analyze:
                    default_model = Model.get_default_model_by_owner()
                    if default_model is None:
                        st.error('用户未设置默认模型，请设置完成后在执行！', icon=':material/error:')
                    else:
                        tags_result = analyze_content_tags(bytes_data, default_model.content)
                        tags = str(tags_result).replace('[', '').replace(']', '')
                else:
                    tags = '请输入'
                st.session_state.file_contents_result.append({'文件名': file_name, '数据集名': dataset_name, '数据标签': tags, '数据内容': bytes_data})

    st.subheader('Step 2：创建数据集', divider=True)
    with st.form('multiple_submit'):
        column_config = {
            '文件名': st.column_config.TextColumn('文件名', width='small'),
            '数据集名': st.column_config.TextColumn('数据集名', width='small'),
            '数据标签': st.column_config.TextColumn('数据标签', width='small'),
            '数据内容': st.column_config.TextColumn('数据内容', width='large', help='点击以查看完整数据')
        }
        edited_datas = st.data_editor(st.session_state.file_contents_result, column_config=column_config,
                                      hide_index=False, num_rows='fixed',
                                      use_container_width=True)
        catalog_name_2 = st.text_input('数据类目', key='catalog_name_2')

        submit_button = st.form_submit_button('提交')
        if submit_button:
            error = False
            index = 0
            for edited_data in edited_datas:
                file_name = edited_data['文件名']
                dataset_name = edited_data['数据集名']
                content = edited_data['数据内容']
                tags = edited_data['数据标签']
                if Dataset.get_dataset_by_owner_with_name(dataset_name) is not None:
                    st.error('第{}行：数据集名已存在，请重新输入！'.format(index), icon=':material/error:')
                    error = True
                    break
                index += 1
            if not error:
                index = 0
                for edited_data in edited_datas:
                    file_name = edited_data['文件名']
                    dataset_name = edited_data['数据集名']
                    content = edited_data['数据内容']
                    tags = edited_data['数据标签']

                    if Dataset.get_dataset_by_owner_with_name(dataset_name) is None:
                        try:
                            dataset = Dataset(catalog=catalog_name_2,
                                              name=dataset_name,
                                              owner=st.session_state.current_username,
                                              channel='flatfile',
                                              source=file_name,
                                              content=content,
                                              tags=tags)
                            session.add(dataset)
                            session.commit()
                        except Exception as e:
                            session.rollback()
                            st.error('第{}行：数据集创建失败，错误原因：{}！'.format(index, e), icon=':material/error:')
                            break
                    index += 1
            if not error:
                st.success('数据集创建成功！', icon=':material/done:')
