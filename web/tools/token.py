import os
import time
from authlib.jose import jwt


def generate_token(user, action, **kwargs):
    secret_key = os.environ.get('SECRET_KEY')
    header = {'alg': 'HS256'}
    data = {'user': user, 'action': action, 'timestamp': time.time()}
    data.update(**kwargs)
    return jwt.encode(header=header, payload=data, key=secret_key)


def validate_token(user, action, token):
    key = os.environ.get('SECRET_KEY')
    try:
        data = jwt.decode(token, key)
    except Exception as e:
        raise e

    if data['user'] == user and data['action'] == action and data['timestamp'] >= time.time()-900:
        return True
    else:
        return False