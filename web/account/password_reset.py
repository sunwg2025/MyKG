import streamlit as st
import time
from web.tools.mail import send_reset_password_email
from web.database.user import User
from web.database import session
from web.tools.validator import check_email_format, check_password_format, check_username_format
from web.tools.token import generate_token, validate_token


if 'reset_password_sendmail_time' not in st.session_state:
    st.session_state.reset_password_sendmail_time = None

if 'reset_password_validate_success' not in st.session_state:
    st.session_state.reset_password_validate_success = False

st.session_state.current_page = 'password_reset_page'
st.header('密码重置')

st.subheader('Step 1：发送验证码', divider=True)
with st.form('sendmail'):
    email = st.text_input('邮箱地址', key='email')

    sendmail_button = st.form_submit_button('发送验证邮件')
    if sendmail_button:
        error = False
        if st.session_state.reset_password_sendmail_time is not None:
            if st.session_state.reset_password_sendmail_time > time.time() - 900:
                st.error('验证邮件已发送，15分钟内仅可发送一次！', icon=':material/error:')
                error = True
        if not check_email_format(email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(email) is None and not error:
            st.error('该邮箱地址未被注册，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_username(st.session_state.current_username).email != email and not error:
            st.error('该邮箱地址与当前登入用户不匹配，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            confirm_code = generate_token(user=st.session_state.current_username, action='reset_password').decode('utf-8')
            try:
                send_reset_password_email(email, st.session_state.current_username, confirm_code)
                st.session_state.reset_password_sendmail_time = time.time()
                st.success('邮件发送成功，请查看邮件中的重置验证码（有效期：15分钟）并输入！', icon=':material/done:')
            except Exception as e:
                st.error('邮件发送失败，错误原因：{}！'.format(e), icon=':material/error:')

st.subheader('Step 2：校验验证码', divider=True)
with st.form('validate'):
    token = st.text_area('验证码', height=80, help='请输入验证邮件中的注册验证码', key='token')

    validate_button = st.form_submit_button('验证')
    if validate_button:
        error = False
        if token == '':
            st.error('请输入邮件中的重置验证码！', icon=':material/error:')
            error = True
        if not error:
            try:
                if not validate_token(user=st.session_state.current_username, action='reset_password', token=token):
                    st.error('验证码校验失败，请检查是否正确输入！', icon=':material/error:')
                    error = True
                st.session_state.reset_password_validate_success = True
                st.success('验证码校验成功，请输入新密码！', icon=':material/done:')
            except Exception as e:
                st.error('验证码校验失败，错误原因：{}！'.format(e), icon=':material/error:')
                error = True

st.subheader('Step 3：输入新密码', divider=True)
with st.form('reset'):
    new_password = st.text_input('新密码', type='password', help='8-16个字符，需包含大、小写字母和数字', key='new_password')
    new_password2 = st.text_input('新密码确认', type='password', help='8-16个字符，需包含大、小写字母和数字', key='new_password2')

    reset_button = st.form_submit_button('重置密码')
    if reset_button:
        error = False
        if not st.session_state.reset_password_validate_success:
            st.error('请首先完成密码重置校验！', icon=':material/error:')
            error = True
        if not check_password_format(new_password) and not error:
            st.error('新密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(new_password2) and not error:
            st.error('新确认密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if new_password != new_password2 and not error:
            st.error('新密码与新确认密码不一致，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                user = User.get_user_by_username(st.session_state.current_username)
                user.update_password(new_password)
                st.success('用户更新密码成功！', icon=':material/done:')
            except Exception as e:
                session.rollback()
                st.error('用户更新密码失败，错误原因：{}！'.format(e), icon=':material/error:')
