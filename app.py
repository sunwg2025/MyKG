import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title='知识图谱系统V1.0', page_icon=':material/cognition:')
st.sidebar.title('知识图谱系统V1.0')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'logged_out' not in st.session_state:
    st.session_state.logged_out = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_username' not in st.session_state:
    st.session_state.current_username = ''
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'app_main'

# 账号权限
user_login_page = st.Page('web/account/user_login.py', title='登入', icon=':material/login:')
user_logout_page = st.Page('web/account/user_logout.py', title='登出', icon=':material/logout:')
user_create_page = st.Page('web/account/user_create.py', title='用户创建', icon=':material/person_add:')
password_reset_page = st.Page('web/account/password_reset.py', title='密码重置', icon=':material/lock_reset:')
email_reset_page = st.Page('web/account/email_reset.py', title='邮箱重置', icon=':material/email:')

# 数据集管理
input_dataset_page = st.Page('web/dataset/input_dataset.py', title='输入数据集', icon=':material/keyboard:')
flatfile_dataset_page = st.Page('web/dataset/flatfile_dataset.py', title='文本数据集', icon=':material/insert_drive_file:')
dataset_modify_page = st.Page('web/dataset/dataset_modify.py', title='数据集变更', icon=':material/folder_copy:')

# 提示词管理
prompt_create_page = st.Page('web/prompt/prompt_create.py', title='提示词创建', icon=':material/sms:')
prompt_modify_page = st.Page('web/prompt/prompt_modify.py', title='提示词变更', icon=':material/event_note:')

# 模型管理
model_create_page = st.Page('web/model/model_create.py', title='模型创建', icon=':material/smart_toy:')
model_modify_page = st.Page('web/model/model_modify.py', title='模型变更', icon=':material/memory:')

# 知识库管理
knowledge_create_page = st.Page('web/knowledge/knowledge_create.py', title='知识库创建', icon=':material/content_paste:')
knowledge_modify_page = st.Page('web/knowledge/knowledge_modify.py', title='知识条目变更', icon=':material/list:')
knowledge_manage_page = st.Page('web/knowledge/knowledge_manage.py', title='知识库管理', icon=':material/content_paste_go:')
knowledge_delete_page = st.Page('web/knowledge/knowledge_delete.py', title='知识库删除', icon=':material/content_paste_off:')

# 知识实验室
experiment_create_page = st.Page('web/laboratory/experiment_create.py', title='知识实验创建', icon=':material/science:')
experiment_execute_page = st.Page('web/laboratory/experiment_execute.py', title='知识实验执行', icon=':material/play_lesson:')
entity_extract_page = st.Page('web/knowledge_extract/entity_extract.py', title='实体抽取', icon=':material/rectangle:')
attribute_extract_page = st.Page('web/knowledge_extract/attribute_extract.py', title='属性抽取', icon=':material/edit_attributes:')
relation_extract_page = st.Page('web/knowledge_extract/relation_extract.py', title='关系抽取', icon=':material/linear_scale:')

# 知识应用
question_and_answer_page = st.Page('web/knowledge_application/question_and_answer.py', title='知识问答', icon=':material/question_mark:')

# 工作流
workflow_create_page = st.Page('web/workflow/workflow_create.py', title='工作流创建', icon=':material/moving:')
workflow_execute_page = st.Page('web/workflow/workflow_execute.py', title='工作流执行', icon=':material/play_circle:')

# 系统管理
quick_guide_page = st.Page('web/system/quick_guide.py', title='快速指南', icon=':material/description:')
admin_prompt_create_page = st.Page('web/system/admin_prompt_create.py', title='提示词创建', icon=':material/edit_calendar:')
model_template_create_page = st.Page('web/system/model_template_create.py', title='模型模板创建', icon=':material/add_chart:')
model_template_modify_page = st.Page('web/system/model_template_modify.py', title='模型模板变更', icon=':material/draw:')
system_prompt_modify_page = st.Page('web/system/system_prompt_modify.py', title='工具提示词变更', icon=':material/construction:')
issue_create_page = st.Page('web/system/issue_create.py', title='问题提交', icon=':material/report_problem:')
issue_modify_page = st.Page('web/system/issue_modify.py', title='问题更新', icon=':material/auto_fix:')

if st.session_state.logged_in:
    if st.session_state.is_admin:
        pg = st.navigation(
            {
                '账号权限': [user_logout_page, password_reset_page, email_reset_page],
                '提示词管理': [prompt_create_page, prompt_modify_page],
                '模型管理': [model_create_page, model_modify_page],
                '数据准备': [input_dataset_page, flatfile_dataset_page, dataset_modify_page],
                '知识库管理': [knowledge_create_page, knowledge_modify_page, knowledge_manage_page, knowledge_delete_page],
                '知识实验室': [experiment_create_page, experiment_execute_page, entity_extract_page, attribute_extract_page, relation_extract_page],
                '工作流管理': [workflow_create_page, workflow_execute_page],
                '知识库应用': [question_and_answer_page],
                '系统管理': [admin_prompt_create_page, model_template_create_page, model_template_modify_page, system_prompt_modify_page, issue_modify_page],
                '系统说明': [quick_guide_page, issue_create_page],
            }
        )
    else:
        pg = st.navigation(
            {
                '账号权限': [user_logout_page, password_reset_page, email_reset_page],
                '提示词管理': [prompt_create_page, prompt_modify_page],
                '模型管理': [model_create_page, model_modify_page],
                '数据准备': [input_dataset_page, flatfile_dataset_page, dataset_modify_page],
                '知识库管理': [knowledge_create_page, knowledge_modify_page, knowledge_manage_page, knowledge_delete_page],
                '知识实验室': [experiment_create_page, experiment_execute_page, entity_extract_page, attribute_extract_page, relation_extract_page],
                '工作流管理': [workflow_create_page, workflow_execute_page],
                '知识库应用': [question_and_answer_page],
                '系统说明': [quick_guide_page, issue_create_page],
            }
        )

else:
    pg = st.navigation(
        {
            '账号权限': [user_login_page, user_create_page],
            '系统说明': [quick_guide_page, issue_create_page],
        }
    )

pg.run()

