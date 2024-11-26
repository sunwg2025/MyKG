import streamlit as st
from web.database.issue import Issue
from datetime import datetime

st.header('系统问题解决')
st.session_state.current_page = 'issue_modify_page'

with st.form('更新问题'):
    my_unfixed_issues = []
    for issue in Issue.get_issues_by_fixed(False):
        my_unfixed_issues.append('{}: 【{}】【{}】'.format(issue.id, issue.page, issue.title))
    unfixed_issue_select = st.selectbox('选择未解决问题', options=my_unfixed_issues)

    if unfixed_issue_select is not None:
        issue_id = unfixed_issue_select.split(':')[0]
        issue = Issue.get_issues_by_id(issue_id)
        st.text('问题编号：{}'.format(issue.id))
        st.text('问题提交人：{}'.format(issue.owner))
        st.text('问题页面：{}'.format(issue.page))
        st.text('问题标题：{}'.format(issue.title))
        st.text('问题详情：{}'.format(issue.detail))

        is_fixed = st.toggle("已解决", value=issue.fixed)
        comment = st.text_area('问题备注', height=240, max_chars=4096)

    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if unfixed_issue_select is None:
            st.error('请先选择问题！', icon=':material/error:')
            error = True
        if not error:
            try:
                issue_id = unfixed_issue_select.split(':')[0]
                issue = Issue.get_issues_by_id(issue_id)
                issue.update_issue_to_fixed(is_fixed, comment)
                st.success('系统问题更新成功！', icon=':material/done:')
            except Exception as e:
                st.error('系统问题更新失败，错误原因：{}！'.format(e), icon=':material/error:')

with st.container(border=True):
    st.text('已解决问题列表')
    my_fixed_issues = Issue.get_issues_by_fixed(True)
    fixed_data = []
    for issue in my_fixed_issues:
        fixed_data.append({'问题编号': issue.id, '提交时间': issue.create_at, '解决状态': issue.fixed, '问题标题': issue.title,
                           '问题详情': issue.detail, '问题回复': issue.comment})
    column_config = {
        '问题编号': st.column_config.NumberColumn('问题编号', width='small'),
        '提交时间': st.column_config.DatetimeColumn('提交时间', width='small'),
        '解决状态': st.column_config.CheckboxColumn('解决状态', width='small'),
        '问题标题': st.column_config.TextColumn('问题标题', width='large', help='点击以查看完整数据'),
        '问题详情': st.column_config.TextColumn('问题详情', width='large', help='点击以查看完整数据'),
        '问题回复': st.column_config.TextColumn('问题回复', width='large', help='点击以查看完整数据')
    }
    unfixed_edited_datas = st.data_editor(fixed_data, column_config=column_config, hide_index=True, num_rows='fixed',
                                          use_container_width=True)
