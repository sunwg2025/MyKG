import argparse
from dotenv import load_dotenv
load_dotenv()
from web.database.user import User
from web.database import session

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
    session.add(user)
    session.commit()
    print('管理员创建成功！')
