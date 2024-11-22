import streamlit as st
import math
from web.database.dataset import Dataset
from web.tools.dataset import split_structured_data, get_csv_row_count, get_csv_file_header, split_structured_csv_data
from web.tools.dataset import create_dataframe_from_text, create_dataframe_from_csv
from web.database.dataset_split import Dataset_Split
from web.database import session
import pandas as pd
import io
from io import StringIO

st.header('结构化数据集创建')
st.session_state.current_page = 'structured_create_page'

data_type_select = st.selectbox('选择数据来源', options=['数据录入', 'CSV文件', 'TXT文件', 'JDBC表'])

dataset_contents_detail = []
channel = ''

if data_type_select == '数据录入':
    st.subheader('Step 1：录入数据', divider=True)
    with st.container(border=True):
        input_dataset_content = st.text_area('数据内容', height=480, key='input_dataset_content')

        columns_separator = st.text_input('列分隔符', value=',', key='columns_separator')
        has_header = st.toggle('是否含有标题', help='数据是否包含标题行')

        input_files_total_rows = 0
        input_files_total_size = 0
        if input_dataset_content.strip():
            input_dataframe = create_dataframe_from_text(input_dataset_content, columns_separator, has_header)
            input_files_total_size = len(input_dataset_content)
            input_files_total_rows = input_dataframe.shape[0]
            tmp_uploaded_file_parse = {'name': 'KeyBoard',
                                       'content': input_dataframe,
                                       'size': input_dataframe.shape[0]}
            dataset_contents_detail.append(tmp_uploaded_file_parse)
            st.dataframe(input_dataframe, use_container_width=True, height=360)
        st.text('总记录数：{}'.format(input_files_total_rows))
        st.text('总字符数：{}'.format(input_files_total_size))
        channel = 'structured_keyboard'
elif data_type_select == 'CSV文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['csv'], accept_multiple_files=True)

        has_header = st.toggle('是否含有标题', help='数据是否包含标题行')

        input_files_total_size = 0
        input_files_total_rows = 0
        input_files_max_size = 0
        input_files_max_rows = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            file_content = StringIO(uploaded_file.getvalue().decode('utf-8')).getvalue()
            input_dataframe = create_dataframe_from_csv(file_content, has_header)

            my_uploaded_files.append("{}: 文件名【{}】 记录数【{}】".format(ind, uploaded_file.name, input_dataframe.shape[0]))

            tmp_uploaded_file_parse = {'name': uploaded_file.name.rsplit('.', 1)[0],
                                       'content': input_dataframe,
                                       'size': input_dataframe.shape[0]}
            dataset_contents_detail.append(tmp_uploaded_file_parse)

            input_files_total_size += uploaded_file.size
            input_files_total_rows += input_dataframe.shape[0]
            input_files_max_size = uploaded_file.size if uploaded_file.size > input_files_max_size \
                else input_files_max_size
            input_files_max_rows = input_dataframe.shape[0] if input_dataframe.shape[0] > input_files_max_rows \
                else input_files_max_rows
            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = dataset_contents_detail[int(ind_select)]
            st.dataframe(dataset_content_select['content'], use_container_width=True, height=360)

        st.text('汇总：记录数【{}】    字符数【{}】'.format(input_files_total_rows, input_files_total_size))
        st.text('单文件：最大记录数【{}】    最大字符数【{}】'.format(input_files_max_rows, input_files_max_size))
        channel = 'structured_csv'

elif data_type_select == 'TXT文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['txt', 'dat'], accept_multiple_files=True)

        columns_separator = st.text_input('列分隔符', value=',', key='columns_separator')
        has_header = st.toggle('是否含有标题', help='数据是否包含标题行')

        input_files_total_size = 0
        input_files_total_rows = 0
        input_files_max_size = 0
        input_files_max_rows = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            file_content = StringIO(uploaded_file.getvalue().decode('utf-8')).getvalue()
            input_dataframe = create_dataframe_from_text(file_content, columns_separator, has_header)

            my_uploaded_files.append("{}: 文件名【{}】 记录数【{}】".format(ind, uploaded_file.name, input_dataframe.shape[0]))

            tmp_uploaded_file_parse = {'name': uploaded_file.name.rsplit('.', 1)[0],
                                       'content': input_dataframe,
                                       'size': input_dataframe.shape[0]}
            dataset_contents_detail.append(tmp_uploaded_file_parse)

            input_files_total_size += uploaded_file.size
            input_files_total_rows += input_dataframe.shape[0]
            input_files_max_size = uploaded_file.size if uploaded_file.size > input_files_max_size \
                else input_files_max_size
            input_files_max_rows = input_dataframe.shape[0] if input_dataframe.shape[0] > input_files_max_rows \
                else input_files_max_rows
            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = dataset_contents_detail[int(ind_select)]
            st.dataframe(dataset_content_select['content'], use_container_width=True, height=360)

        st.text('汇总：记录数【{}】    字符数【{}】'.format(input_files_total_rows, input_files_total_size))
        st.text('单文件：最大记录数【{}】    最大字符数【{}】'.format(input_files_max_rows, input_files_max_size))
        channel = 'structured_txt'

st.subheader('Step 2：数据分片', divider=True)
with st.container(border=True):
    split_row_limit = st.slider('记录数限制', 1, 200, 10)
    split_size_limit = st.slider('字符数限制', 1024, 8192, 2048)

    estimate_row_split_cnt = math.ceil(input_files_total_rows / split_row_limit)
    estimate_size_split_cnt = math.ceil(input_files_total_size / split_size_limit)
    st.text('预估分片数：{}'.format(max(estimate_row_split_cnt, estimate_size_split_cnt)))

st.subheader('Step 3：设置属性', divider=True)
with st.container(border=True):
    if data_type_select == '数据录入':
        is_files_combine = st.toggle('是否合并数据集', disabled=True, help='所有文件合并为一个数据集', value=True)
    else:
        is_files_combine = st.toggle('是否合并数据集', help='所有文件合并为一个数据集', value=False)

    dataset_tags = st.text_input('数据标签', help='数据内容关键词，逗号分隔', key='dataset_tags')
    dataset_catalog = st.text_input('数据类目', key='dataset_catalog')
    if is_files_combine:
        dataset_name = st.text_input('数据集名', key='dataset_name')
    else:
        dataset_prefix = st.text_input('数据集名前缀', key='dataset_name', help='数据集名为数据集名前缀+文件名')

    if st.button('提交'):
        error = False
        if input_files_total_size == 0:
            st.error('数据内容为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            if is_files_combine:
                if dataset_name.strip() == '':
                    st.error('数据集名不能为空，请重新输入！', icon=':material/error:')
                    error = True
            else:
                if dataset_prefix.strip() == '':
                    st.error('数据集名前缀不能为空，请重新输入！', icon=':material/error:')
                    error = True
        if dataset_catalog.strip() == '' and not error:
            st.error('数据类目不能为空，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            if is_files_combine:
                if Dataset.get_dataset_by_owner_with_name(dataset_name) is not None:
                    st.error('用户下同名数据集已存在，请重新输入！', icon=':material/error:')
                    error = True
            else:
                for dataset_content_detail in dataset_contents_detail:
                    tmp_dataset_name = dataset_prefix + '.' + dataset_content_detail['name']
                    if Dataset.get_dataset_by_owner_with_name(tmp_dataset_name) is not None:
                        st.error('用户下同名数据集【{}】已存在，请重新输入！'.format(tmp_dataset_name), icon=':material/error:')
                        error = True
        if not error:
            all_dataset_contents = []
            for dataset_content_detail in dataset_contents_detail:
                all_dataset_contents.append(dataset_content_detail['content'])

            if is_files_combine:
                files_content_combine = pd.concat(all_dataset_contents, ignore_index=True)
                all_dataset_contents = [files_content_combine]

            ind = 0
            try:
                for dataset_content in all_dataset_contents:
                    dataset_splits = split_structured_csv_data(dataset_content, split_row_limit, split_size_limit)
                    if is_files_combine:
                        tmp_dataset_name = dataset_name
                    else:
                        tmp_dataset_name = dataset_prefix + '.' + dataset_contents_detail[ind]['name']

                    dataset_total_chr_cnt = 0
                    for dataset_split in dataset_splits:
                        dataset_total_chr_cnt += len(dataset_split)

                    if len(all_dataset_contents) == 1 and len(dataset_contents_detail) > 1:
                        file_names = [item['name'] for item in dataset_contents_detail]
                        source = ','.join(file_names)
                    else:
                        source = dataset_contents_detail[ind]['name']

                    dataset = Dataset(catalog=dataset_catalog,
                                      name=tmp_dataset_name,
                                      owner=st.session_state.current_username,
                                      channel=channel,
                                      source=source,
                                      tags=dataset_tags,
                                      total_size=dataset_total_chr_cnt,
                                      split_count=len(dataset_splits))
                    session.add(dataset)
                    dataset_un_commit = Dataset.get_dataset_by_owner_with_name(tmp_dataset_name)
                    split_ind = 1
                    summary_content = ''
                    for dataset_split in dataset_splits:
                        if split_ind < 10:
                            split_name = '{}_0{}'.format(tmp_dataset_name, str(split_ind))
                        else:
                            split_name = '{}_{}'.format(tmp_dataset_name, str(split_ind))

                        dataset_split = Dataset_Split(name=split_name,
                                                      owner=st.session_state.current_username,
                                                      dataset_id=dataset_un_commit.id,
                                                      split_seq=split_ind,
                                                      total_size=len(dataset_split),
                                                      content=dataset_split)
                        split_ind += 1
                        session.add(dataset_split)
                    ind += 1
                session.commit()
                st.success('数据集创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('数据集创建失败，错误原因：{}！'.format(e), icon=':material/error:')



