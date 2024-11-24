import streamlit as st
import math
from web.database.dataset import Dataset
from web.database.dataset_split import Dataset_Split
from web.database.model import Model
from web.database import session
from web.tools.dataset import split_unstructured_data, parse_unstructured_pdf_data
from web.tools.dataset import parse_unstructured_video_data, parse_unstructured_audio_data
from web.tools.model import analyze_content_summary
from io import StringIO

st.header('非结构化数据集创建')

data_type_select = st.selectbox('选择数据来源', options=['数据录入', 'TXT文件', 'PDF文件', '音频文件', '视频文件'])

if 'dataset_contents_detail' not in st.session_state:
    st.session_state.dataset_contents_detail = []

current_page = 'unstructured_create_page'
if st.session_state.current_page != current_page:
    st.session_state.dataset_contents_detail = []
st.session_state.current_page = 'unstructured_create_page'

channel = ''

if data_type_select == '数据录入':
    st.subheader('Step 1：录入数据', divider=True)
    with st.container(border=True):
        st.session_state.dataset_contents_detail = []
        input_dataset_content = st.text_area('数据内容', height=480, key='input_dataset_content')
        input_files_total_size = len(input_dataset_content)
        st.text('总字符数：{}'.format(input_files_total_size))
        tmp_uploaded_file_parse = {'name': 'KeyBoard',
                                   'content': input_dataset_content,
                                   'size': len(input_dataset_content)}
        st.session_state.dataset_contents_detail.append(tmp_uploaded_file_parse)
        channel = 'unstructured_keyboard'
elif data_type_select == 'TXT文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['txt'], accept_multiple_files=True)

        input_files_total_size = 0
        input_files_max_size = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            uploaded_file_name = uploaded_file.name.rsplit('.', 1)[0]
            uploaded_file_parsed = [item['name'] for item in st.session_state.dataset_contents_detail]
            if uploaded_file_name not in uploaded_file_parsed:
                uploaded_file_content = StringIO(uploaded_file.getvalue().decode('utf-8')).getvalue()
                tmp_uploaded_file_parse = {'name': uploaded_file_name,
                                           'content': uploaded_file_content,
                                           'size': len(uploaded_file_content)}
                st.session_state.dataset_contents_detail.append(tmp_uploaded_file_parse)
            else:
                uploaded_file_content = st.session_state.dataset_contents_detail['uploaded_file_name']['content']

            my_uploaded_files.append("{}: 文件名【{}】 字符数【{}】".format(ind, uploaded_file.name, len(uploaded_file_content)))
            input_files_total_size += len(uploaded_file_content)
            input_files_max_size = len(uploaded_file_content) if len(uploaded_file_content) > input_files_max_size \
                else input_files_max_size
            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = st.session_state.dataset_contents_detail[int(ind_select)]
            st.text_area('数据内容', value=dataset_content_select['content'], height=360, label_visibility='collapsed')

        st.text('汇总：字符数【{}】'.format(input_files_total_size))
        st.text('单文件：最大字符数【{}】'.format(input_files_max_size))
        channel = 'unstructured_txt'
elif data_type_select == 'PDF文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['pdf'], accept_multiple_files=True)

        input_files_total_size = 0
        input_files_max_size = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            uploaded_file_name = uploaded_file.name.rsplit('.', 1)[0]
            uploaded_file_parsed = [item['name'] for item in st.session_state.dataset_contents_detail]
            if uploaded_file_name not in uploaded_file_parsed:
                uploaded_file_content = parse_unstructured_pdf_data(uploaded_file.getvalue())
                tmp_uploaded_file_parse = {'name': uploaded_file_name,
                                           'content': uploaded_file_content,
                                           'size': len(uploaded_file_content)}
                st.session_state.dataset_contents_detail.append(tmp_uploaded_file_parse)
            else:
                uploaded_file_content = st.session_state.dataset_contents_detail[uploaded_file_name]['content']

            my_uploaded_files.append("{}: 文件名【{}】 字符数【{}】".format(ind, uploaded_file.name, len(uploaded_file_content)))
            input_files_total_size += len(uploaded_file_content)
            input_files_max_size = len(uploaded_file_content) if len(uploaded_file_content) > input_files_max_size \
                else input_files_max_size

            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = st.session_state.dataset_contents_detail[int(ind_select)]
            st.text_area('数据内容', value=dataset_content_select['content'], height=360, label_visibility='collapsed')

        st.text('汇总：字符数【{}】'.format(input_files_total_size))
        st.text('单文件：最大字符数【{}】'.format(input_files_max_size))
        channel = 'unstructured_pdf'
elif data_type_select == '音频文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['wav'], accept_multiple_files=True)

        input_files_total_size = 0
        input_files_max_size = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            uploaded_file_name = uploaded_file.name.rsplit('.', 1)[0]
            uploaded_file_parsed = [item['name'] for item in st.session_state.dataset_contents_detail]
            if uploaded_file_name not in uploaded_file_parsed:
                uploaded_file_content = parse_unstructured_audio_data(uploaded_file.getvalue(), uploaded_file.name)
                tmp_uploaded_file_parse = {'name': uploaded_file_name,
                                           'content': uploaded_file_content,
                                           'size': len(uploaded_file_content)}
                st.session_state.dataset_contents_detail.append(tmp_uploaded_file_parse)
            else:
                uploaded_file_content = st.session_state.dataset_contents_detail[uploaded_file_name]['content']

            my_uploaded_files.append("{}: 文件名【{}】 字符数【{}】".format(ind, uploaded_file.name, len(uploaded_file_content)))
            input_files_total_size += len(uploaded_file_content)
            input_files_max_size = len(uploaded_file_content) if len(uploaded_file_content) > input_files_max_size \
                else input_files_max_size
            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = st.session_state.dataset_contents_detail[int(ind_select)]
            st.text_area('数据内容', value=dataset_content_select['content'], height=360, label_visibility='collapsed')

        st.text('汇总：字符数【{}】'.format(input_files_total_size))
        st.text('单文件：最大字符数【{}】'.format(input_files_max_size))
        channel = 'unstructured_audio'
elif data_type_select == '视频文件':
    st.subheader('Step 1：选择文件', divider=True)
    with st.container(border=True):
        uploaded_files = st.file_uploader('选择单个或多个文件', type=['mp4', 'mov'], accept_multiple_files=True)

        input_files_total_size = 0
        input_files_max_size = 0
        my_uploaded_files = []
        ind = 0
        for uploaded_file in uploaded_files:
            uploaded_file_name = uploaded_file.name.rsplit('.', 1)[0]
            uploaded_file_parsed = [item['name'] for item in st.session_state.dataset_contents_detail]
            if uploaded_file_name not in uploaded_file_parsed:
                uploaded_file_content = parse_unstructured_video_data(uploaded_file.getvalue(), uploaded_file.name)
                tmp_uploaded_file_parse = {'name': uploaded_file_name,
                                           'content': uploaded_file_content,
                                           'size': len(uploaded_file_content)}
                st.session_state.dataset_contents_detail.append(tmp_uploaded_file_parse)
            else:
                uploaded_file_content = st.session_state.dataset_contents_detail[uploaded_file_name]['content']

            my_uploaded_files.append("{}: 文件名【{}】 字符数【{}】".format(ind, uploaded_file.name, len(uploaded_file_content)))
            input_files_total_size += len(uploaded_file_content)
            input_files_max_size = len(uploaded_file_content) if len(uploaded_file_content) > input_files_max_size \
                else input_files_max_size


            ind += 1

        uploaded_file_select = st.selectbox('数据预览', options=my_uploaded_files)
        if uploaded_file_select is not None:
            ind_select = uploaded_file_select.split(':')[0]
            dataset_content_select = st.session_state.dataset_contents_detail[int(ind_select)]
            st.text_area('数据内容', value=dataset_content_select['content'], height=360, label_visibility='collapsed')

        st.text('汇总：字符数【{}】'.format(input_files_total_size))
        st.text('单文件：最大字符数【{}】'.format(input_files_max_size))
        channel = 'unstructured_video'

st.subheader('Step 2：数据分片', divider=True)
with st.container(border=True):
    split_size_limit = st.slider('字符数限制', 256, 8192, 2048)
    split_overlap_limit = st.slider('重叠字符数', 0, 400, 200)

    is_attach_summary = st.toggle('是否附加摘要', help='是否附加通过大模型抽取的前文摘要', disabled=False)

    estimate_data_splits_cnt = math.ceil(input_files_total_size / (split_size_limit - split_overlap_limit))
    st.text('预估分片数：{}'.format(estimate_data_splits_cnt))

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
                for dataset_content_detail in st.session_state.dataset_contents_detail:
                    tmp_dataset_name = dataset_prefix + '.' + dataset_content_detail['name']
                    if Dataset.get_dataset_by_owner_with_name(tmp_dataset_name) is not None:
                        st.error('用户下同名数据集【{}】已存在，请重新输入！'.format(tmp_dataset_name), icon=':material/error:')
                        error = True
        if is_attach_summary and not error:
            default_model = Model.get_default_model_by_owner()
            if default_model is None:
                st.error('用户未设置默认模型配置，请设置默认模型或关闭附加摘要功能！', icon=':material/error:')
                error = True
        if not error:
            all_dataset_contents = []
            for dataset_content_detail in st.session_state.dataset_contents_detail:
                all_dataset_contents.append(dataset_content_detail['content'])

            if is_files_combine:
                files_content_combine = '\n'.join(all_dataset_contents)
                all_dataset_contents = [files_content_combine]

            ind = 0
            try:
                for dataset_content in all_dataset_contents:
                    dataset_splits = split_unstructured_data(dataset_content, split_size_limit, split_overlap_limit)
                    if is_files_combine:
                        tmp_dataset_name = dataset_name
                    else:
                        tmp_dataset_name = dataset_prefix + '.' + st.session_state.dataset_contents_detail[ind]['name']

                    dataset_total_chr_cnt = 0
                    for dataset_split in dataset_splits:
                        dataset_total_chr_cnt += len(dataset_split)

                    if len(all_dataset_contents) == 1 and len(st.session_state.dataset_contents_detail) > 1:
                        file_names = [item['name'] for item in st.session_state.dataset_contents_detail]
                        source = ','.join(file_names)
                    else:
                        source = st.session_state.dataset_contents_detail[ind]['name']

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

                        dataset_content_with_summary = dataset_split
                        if is_attach_summary:
                            if summary_content == '':
                                summary_content = analyze_content_summary(dataset_split, default_model.content)
                            else:
                                dataset_content_with_summary = summary_content + '\n' + dataset_content_with_summary
                                summary_content = analyze_content_summary(dataset_content_with_summary,
                                                                          default_model.content)

                        dataset_split = Dataset_Split(name=split_name,
                                                      owner=st.session_state.current_username,
                                                      dataset_id=dataset_un_commit.id,
                                                      split_seq=split_ind,
                                                      total_size=len(dataset_content_with_summary),
                                                      content=dataset_content_with_summary)
                        split_ind += 1
                        session.add(dataset_split)
                    ind += 1
                session.commit()
                st.success('数据集创建成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('数据集创建失败，错误原因：{}！'.format(e), icon=':material/error:')
