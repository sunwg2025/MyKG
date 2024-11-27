import argparse
import os

from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append(os.environ['BASE_DIR'])
from web.database.user import User

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="Administrator Email")
    parser.add_argument("--password", help="Administrator Password")

    args = parser.parse_args()
    user = User(email=args.email,
                username='system',
                password=args.password,
                confirmed=True,
                enabled=True,
                is_admin=True)
    User.create_user(user)
    print('管理员创建成功！')
