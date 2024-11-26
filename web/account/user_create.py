import streamlit as st
import time
from web.tools.mail import send_confirm_email
from web.database.user import User
from web.tools.validator import check_email_format, check_password_format, check_username_format
from web.tools.token import generate_token, validate_token

if 'register_sendmail_time' not in st.session_state:
    st.session_state.register_sendmail_time = None

st.session_state.current_page = 'user_create_page'
st.header('用户创建')

st.subheader('Step 1：填写基本信息', divider=True)
with st.form('sendmail'):
    email = st.text_input('邮箱地址', key='email')
    username = st.text_input('用户名', help='6-18个字符，可使用字母、数字、下划线，需以字母开头', key='username')
    password = st.text_input('密码', type='password', help='8-16个字符，需包含大、小写字母和数字', key='password')
    password2 = st.text_input('确认密码', type='password', help='8-16个字符，需包含大、小写字母和数字', key='password2')

    sendmail_submitted = st.form_submit_button('发送验证邮件')
    if sendmail_submitted:
        error = False
        if st.session_state.register_sendmail_time is not None:
            if st.session_state.register_sendmail_time > time.time() - 900:
                st.error('验证邮件已发送，15分钟内仅可发送一次！', icon=':material/error:')
                error = True
        if not check_email_format(email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(email) is not None and not error:
            st.error('该邮箱地址已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not check_username_format(username) and not error:
            st.error('用户名输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_username(username) is not None and not error:
            st.error('该用户名已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(password) and not error:
            st.error('密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(password2) and not error:
            st.error('确认密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if password != password2 and not error:
            st.error('密码与确认密码不一致，请重新输入！', icon=':material/error:')
            error = True

        if not error:
            confirm_code = generate_token(user=username, action='register').decode('utf-8')
            try:
                send_confirm_email(email, username, confirm_code)
                st.session_state.register_sendmail_time = time.time()
                st.success('邮件发送成功，请查看邮件中的注册验证码（有效期：15分钟）并输入！', icon=':material/done:')
            except Exception as e:
                st.error('邮件发送失败，错误原因：{}！'.format(e), icon=':material/error:')

st.subheader('Step 2：校验验证码', divider=True)
with st.form('register'):
    token = st.text_area('验证码', height=80, help='请输入验证邮件中的注册验证码', key='token')

    register_submitted = st.form_submit_button('验证并注册')
    if register_submitted:
        error = False
        if token == '':
            st.error('请输入邮件中的注册验证码！', icon=':material/error:')
            error = True
        if not check_email_format(email) and not error:
            st.error('邮箱地址输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_email(email) is not None and not error:
            st.error('该邮箱地址已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not check_username_format(username) and not error:
            st.error('用户名输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if User.get_user_by_username(username) is not None and not error:
            st.error('该用户名已被注册，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(password) and not error:
            st.error('密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if not check_password_format(password2) and not error:
            st.error('确认密码输入不正确，请重新输入！', icon=':material/error:')
            error = True
        if password != password2 and not error:
            st.error('密码与确认密码不一致，请重新输入！', icon=':material/error:')
            error = True
        if not error:
            try:
                if not validate_token(user=username, action='register', token=token):
                    st.error('注册验证码校验失败，请检查是否正确输入！', icon=':material/error:')
                    error = True
            except Exception as e:
                st.error('验证码校验失败，错误原因：{}！'.format(e), icon=':material/error:')
                error = True
        if not error:
            try:
                user = User(email=email,
                            username=username,
                            password=password,
                            confirmed=True,
                            enabled=True)
                User.create_user(user)
                st.success('用户注册成功！', icon=':material/done:')
            except Exception as e:
                st.error('用户创建失败，错误原因：{}！'.format(e), icon=':material/error:')









