import streamlit as st
from web.database.issue import Issue

st.header('系统问题提交')
st.session_state.current_page = 'issue_create_page'

with st.form('submit'):
    all_pages = ['用户创建', '登入', '登出', '密码重置', '邮箱重置', '提示词创建', '提示词变更', '模型创建', '模型变更',
                 '输入数据集', '文本数据集', '数据集变更', '知识库创建', '知识条目变更', '知识库管理', '知识库删除',
                 '知识实验创建', '知识实验执行', '实体抽取', '属性抽取', '关系抽取', '工作流创建', '工作流执行', '知识问答',
                 '快速指南', '其他问题']
    issue_page_select = st.selectbox('选择问题页面', options=all_pages)

    issue_title = st.text_input('问题标题')
    issue_detail = st.text_area('问题详情', height=240, max_chars=4096)

    submit_button = st.form_submit_button('提交')
    if submit_button:
        error = False
        if issue_page_select is None:
            st.error('请选择问题页面！', icon=':material/error:')
            error = True
        if issue_title == '' and not error:
            st.error('请输入问题标题！', icon=':material/error:')
            error = True
        if issue_detail == '' and not error:
            st.error('请输入问题详情！', icon=':material/error:')
            error = True
        if not error:
            try:
                issue = Issue(page=issue_page_select,
                              owner=st.session_state.current_username,
                              title=issue_title,
                              detail=issue_detail,
                              fixed=False)
                Issue.create_issue(issue)
                st.success('系统问题提交成功，会尽快完成修复，谢谢支持！', icon=':material/done:')
            except Exception as e:
                st.error('系统问题提交失败，错误原因：{}！'.format(e), icon=':material/error:')

with st.container(border=True):
    st.text('历史问题')
    my_issues = Issue.get_issues_by_owner()
    data = []
    for issue in my_issues:
        data.append({'问题编号': issue.id, '提交时间': issue.create_at, '解决状态': issue.fixed, '问题标题': issue.title,
                     '问题详情': issue.detail, '问题回复': issue.comment})
    column_config = {
        '问题编号': st.column_config.NumberColumn('问题编号', width='small'),
        '提交时间': st.column_config.DatetimeColumn('提交时间', width='small'),
        '解决状态': st.column_config.CheckboxColumn('解决状态', width='small'),
        '问题标题': st.column_config.TextColumn('问题标题', width='large', help='点击以查看完整数据'),
        '问题详情': st.column_config.TextColumn('问题详情', width='large', help='点击以查看完整数据'),
        '问题回复': st.column_config.TextColumn('问题回复', width='large', help='点击以查看完整数据')
    }
    edited_datas = st.data_editor(data, column_config=column_config, hide_index=True, num_rows='fixed',
                                  use_container_width=True, disabled=True)