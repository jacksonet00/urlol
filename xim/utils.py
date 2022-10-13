from bcrypt import hashpw, checkpw, gensalt


def get_hashed_password(plain_text_password):
    return hashpw(plain_text_password.encode('utf-8'), gensalt())


def check_password(plain_text_password, hashed_password):
    return checkpw(plain_text_password, hashed_password)
