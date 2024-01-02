import jwt
import hashlib
from src.data_store import data_store
from src.error import *


SESSION_ID = 0
SECRET = 'SECRETIVE_MARK'
def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['token'] = []
    store['channels'] = []
    store['dms'] = []
    store['message_id_removed'] = []
    store['all_notifications'] = []
    store['channels_exist'] = []
    store['dms_exist'] = []
    store['messages_exist'] = []
    data_store.set(store)
    return {}

def generate_new_session_id():
    global SESSION_ID
    SESSION_ID += 1
    return SESSION_ID

# helper function

# dictionary as input and string as output
# user_info = {
#     'u_id': 1,
#     'session_id': 1
# }
def encode_jwt(user_info):
    return jwt.encode(user_info, SECRET, algorithm = 'HS256')

# string as input and dictionary as output
# encoded_token = 'abcdefg'
def decode_jwt(encoded_token):
    return jwt.decode(encoded_token, SECRET, algorithms = 'HS256')

# string as input and output
def encode_password_or_reset_code(code):
    return jwt.encode({'code': code}, SECRET, algorithm = 'HS256')

# string as input and output
def decode_password_or_reset_code(code):
    return jwt.decode(code, SECRET, algorithms = 'HS256')['code']

# only used in password and undecipherable
def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# check token whether valid
def check_valid_token(token, token_list):
    if token not in token_list:
        raise AccessError('Invalid Token')
