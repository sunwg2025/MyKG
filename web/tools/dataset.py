import io
import re
import os
import PyPDF2
import pandas as pd
import numpy as np
import streamlit as st
from web.tools import funasr_model
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_structured_data(data_content, row_limit, size_limit):
    split_results = []
    current_chunk = []
    current_size = 0
    for line in data_content.splitlines():
        if line.strip():
            if len(current_chunk) == row_limit or len(line) + current_size >= size_limit:
                split_results.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            else:
                current_chunk.append(line)
                current_size += len(line) + 1
    if len(current_chunk) > 0:
        split_results.append('\n'.join(current_chunk))
    return split_results


def get_csv_row_count(csv_content, has_header):
    if has_header:
        df = pd.read_csv(io.StringIO(csv_content))
    else:
        df = pd.read_csv(io.StringIO(csv_content), header=None)
    return df.shape[0]


def get_csv_file_header(csv_content, has_header):
    header = []
    if has_header:
        df = pd.read_csv(io.StringIO(csv_content))
        for h in df.head(0):
            header.append(h)
    else:
        df = pd.read_csv(io.StringIO(csv_content), header=None)
        for k in df.keys():
            header.append('Col_{}'.format(k))
    return header


def split_structured_csv_data(csv_dataframe, row_limit, size_limit):
    split_results = []
    current_chunk = []
    current_size = 0
    for index, row in csv_dataframe.iterrows():
        row_content = ','.join(str(value) for value in row)
        if len(current_chunk) == row_limit or len(row_content) + current_size >= size_limit:
            split_results.append('\n'.join(current_chunk))
            current_chunk = [row_content]
            current_size = len(row_content)
        else:
            current_chunk.append(row_content)
            current_size += len(row_content) + 1
    if len(current_chunk) > 0:
        split_results.append('\n'.join(current_chunk))
    return split_results


def custom_length_function(text):
    separators = '[.!?。？！]+'
    text_without_separators = re.sub(separators + r'\s*', '', text)
    return len(text_without_separators)


def split_unstructured_data(data_content, size_limit, overlap_limit):
    split_results = []
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[r'[.!?。？！]+'],
        chunk_size=size_limit,
        keep_separator='end',
        chunk_overlap=overlap_limit,
        length_function=custom_length_function,
        is_separator_regex=True
    )
    texts = text_splitter.create_documents([data_content])
    for text in texts:
        split_results.append(text.page_content)
    return split_results


def parse_unstructured_pdf_data(data_content):
    page_results = []
    pdf_document = PyPDF2.PdfReader(io.BytesIO(data_content))
    for page in pdf_document.pages:
        text = page.extract_text()
        page_results.append(text)
    return '\n'.join(page_results)


def save_data_content_to_file(data_content, data_file):
    target_path = os.path.join(os.environ.get('STORAGE_DIR'), st.session_state.current_username)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    target_file = os.path.join(target_path, data_file)
    with open(target_file, 'wb') as file:
        file.write(data_content)
    file.close()
    return target_file


def remove_data_content_file(data_file):
    if os.path.exists(data_file):
        os.remove(data_file)


def parse_unstructured_video_data(data_content, file_name):
    target_file = save_data_content_to_file(data_content, file_name)
    rec_result = funasr_model.generate(target_file)
    remove_data_content_file(target_file)
    return rec_result[0]['text']


def parse_unstructured_audio_data(data_content, file_name):
    target_file = save_data_content_to_file(data_content, file_name)
    rec_result = funasr_model.generate(target_file)
    remove_data_content_file(target_file)
    return rec_result[0]['text']


def get_txt_file_header(header_column, has_header):
    if has_header:
        return header_column
    else:
        header = []
        for k in range(len(header_column)):
            header.append('Col_{}'.format(k))
        return header


def create_dataframe_from_text(data_content, separator, has_header):
    rows = []
    for line in data_content.splitlines():
        if line.strip():
            columns = []
            cols = line.strip().split(separator)
            for col in cols:
                columns.append(col.strip())
            rows.append(columns)
    header = get_txt_file_header(rows[0], has_header)
    if has_header:
        del rows[0]
    df = pd.DataFrame(np.array(rows), columns=header)
    return df


def create_dataframe_from_csv(data_content, has_header):
    if has_header:
        df = pd.read_csv(io.StringIO(data_content))
    else:
        df = pd.read_csv(io.StringIO(data_content), header=None)
        header = []
        for k in range(df.shape[1]):
            header.append('Col_{}'.format(k))
        df.columns = header
    return df


def main():
    aaa="""
    a,b,c
    1,2,3
    """
    df = create_dataframe_from_text(aaa, ',', False)
    print(df.shape[0])
    print(df.map(len).sum().sum())

if __name__ == "__main__":
    main()
