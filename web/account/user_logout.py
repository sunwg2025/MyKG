import streamlit as st

st.header('用户登出')
st.session_state.current_page = 'user_logout_page'

with st.form('logout'):
    username = st.text_input('当前用户', value=st.session_state.current_username, disabled=True, key='username')
    is_admin = st.toggle('管理员', value=st.session_state.is_admin, disabled=True)

    logout_button = st.form_submit_button('登出')
    if logout_button:
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.current_username = ''
        st.success('用户登出成功！', icon=':material/done:')
        st.rerun()
