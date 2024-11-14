import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

confirm_template = """
嗨 {{ username }},

感谢使用知识图谱系统!

请将以下注册验证码输入到用户注册页面中的注册验证输入框中，以完成用户注册流程：

注册验证码：{{ confirm_code }}

祝好！

提示：请不要回复本邮件。
"""

reset_password_template = """
嗨 {{ username }},

感谢使用知识图谱系统!

请将以下重置验证码输入到重置密码页面中的重置验证输入框中，以完成用户重置密码流程：

重置验证码：{{ confirm_code }}

祝好！

提示：请不要回复本邮件。
"""

reset_mail_template = """
嗨 {{ username }},

感谢使用知识图谱系统!

请将以下重置验证码输入到重置邮箱页面中的重置验证输入框中，以完成用户重置邮箱流程：

重置验证码：{{ confirm_code }}

祝好！

提示：请不要回复本邮件。
"""


def send_mail(receiver, subject, content):
    sender = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    mail_server = os.environ.get('MAIL_SERVER')
    mail_port = os.environ.get('MAIL_PORT')

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP(mail_server, mail_port)
        smtpObj.starttls()  # 启用TLS加密
        smtpObj.login(sender, password)  # 登录SMTP服务器
        smtpObj.sendmail(sender, receiver, message.as_string())  # 发送邮件
        smtpObj.quit()  # 关闭连接
    except smtplib.SMTPException as e:
        raise e


def send_confirm_email(receiver, username, confirm_code):
    subject = '知识图谱系统V1.0-注册验证'
    content = confirm_template.replace('{{ username }}', username).replace('{{ confirm_code }}', confirm_code)
    send_mail(receiver, subject, content)


def send_reset_password_email(receiver, username, confirm_code):
    subject = '知识图谱系统V1.0-重置密码验证'
    content = reset_password_template.replace('{{ username }}', username).replace('{{ confirm_code }}', confirm_code)
    send_mail(receiver, subject, content)


def send_reset_mail_email(receiver, username, confirm_code):
    subject = '知识图谱系统V1.0-重置邮箱验证'
    content = reset_mail_template.replace('{{ username }}', username).replace('{{ confirm_code }}', confirm_code)
    send_mail(receiver, subject, content)