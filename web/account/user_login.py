import streamlit as st
from web.database.user import User
from web.database import session
from web.tools.validator import check_email_format, check_password_format

st.header('用户登入')
st.session_state.current_page = 'user_login_page'

with st.form('login'):
    email = st.text_input('邮箱地址', key='email')
    password = st.text_input('密码', type='password', help='8-16个字符，需包含大、小写字母和数字', key='password')
    #keep_status = st.checkbox("保持登陆", key='keep_status')

    login_button = st.form_submit_button('登入')
    if login_button:
        error = False
        if st.session_state.logged_in:
            st.error('用户已登入，请勿重复登入！', icon=':material/error:')
            error = True
        if not check_email_format(email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(email) is None and not error:
            st.error('该邮箱地址未注册用户，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(password) and not error:
            st.error('密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            user = session.query(User).filter(User.email == email).first()
            if user.verify_password(password):
                st.success('用户登入成功！', icon=':material/done:')
                st.session_state.logged_in = True
                st.session_state.is_admin = user.is_admin
                st.session_state.current_username = user.username
                st.rerun()
            else:
                st.error('邮箱地址或密码输入错误，请重新输入！', icon=':material/error:')
