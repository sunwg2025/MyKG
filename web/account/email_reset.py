import streamlit as st
import time
from web.tools.email import send_reset_mail_email
from web.database.user import User
from web.database import session
from web.tools.validator import check_email_format, check_password_format, check_username_format
from web.tools.token import generate_token, validate_token

if 'reset_mail_sendmail_time' not in st.session_state:
    st.session_state.reset_mail_sendmail_time = None

st.session_state.current_page = 'email_reset_page'
st.header('邮箱重置')

st.subheader('Step 1：发送验证码', divider=True)
with st.form('sendmail'):
    password = st.text_input('密码', type='password', help='8-16个字符，需包含大、小写字母和数字', key='password')
    new_email = st.text_input('新邮箱地址', key='new_email')

    sendmail_button = st.form_submit_button('发送验证邮件')
    if sendmail_button:
        error = False
        user = User.get_user_by_username(st.session_state.current_username)
        if st.session_state.reset_mail_sendmail_time is not None:
            if st.session_state.reset_mail_sendmail_time > time.time() - 900:
                st.error('验证邮件已发送，15分钟内仅可发送一次！', icon=':material/error:')
                error = True
        if not user.verify_password(password) and not error:
            st.error('密码输入错误，请重新输入！', icon=':material/error:')
            error = True
        if not check_email_format(new_email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(new_email) is not None and not error:
            st.error('该邮箱地址已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            confirm_code = generate_token(user=st.session_state.current_username, action='reset_mail').decode('utf-8')
            try:
                send_reset_mail_email(new_email, st.session_state.current_username, confirm_code)
                st.session_state.reset_password_sendmail_time = time.time()
                st.success('邮件发送成功，请查看邮件中的重置验证码（有效期：15分钟）并输入！', icon=':material/done:')
            except Exception as e:
                st.error('邮件发送失败，错误原因：{}！'.format(e), icon=':material/error:')

st.subheader('Step 2：校验验证码', divider=True)
with st.form('reset'):
    token = st.text_area('验证码', height=80, help='请输入验证邮件中的注册验证码', key='token')

    reset_button = st.form_submit_button('验证并重置')
    if reset_button:
        error = False
        if token == '':
            st.error('请输入邮件中的重置验证码！', icon=':material/error:')
            error = True
        if not error:
            try:
                if not validate_token(user=st.session_state.current_username, action='reset_mail', token=token):
                    st.error('验证码校验失败，请检查是否正确输入！', icon=':material/error:')
                    error = True
            except Exception as e:
                st.error('验证码校验失败，错误原因：{}！'.format(e), icon=':material/error:')
                error = True
        if not check_email_format(new_email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(new_email) is not None and not error:
            st.error('该邮箱地址已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                user = User.get_user_by_username(st.session_state.current_username)
                user.update_email(new_email)
                st.success('用户邮箱重置成功！', icon=':material/done:')
            except Exception as e:
                st.error('用户邮箱重置失败，错误原因：{}！'.format(e), icon=':material/error:')
                error = True
