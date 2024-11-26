import re


def check_email_format(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    else:
        return False


def check_password_format(password):
    if len(password) < 8 or len(password) > 16:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True


def check_username_format(username):
    if len(username) < 6 or len(username) > 18:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    if not re.match(r'^[a-zA-Z]', username):
        return False
    return True


def check_profile_name_format(profile_name):
    if len(profile_name) < 6 or len(profile_name) > 64:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', profile_name):
        return False
    if not re.match(r'^[a-zA-Z]', profile_name):
        return False
    return True