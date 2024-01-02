from src.data_store import data_store
from src.error import *
from src.other import *

def search_v1(token, query_str):
    result = []
    store = data_store.get()
    # check whether the token is vaild or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    # raise inputerror when the length of query_str does not satisfy the requirement
    if len(query_str) < 1 or len(query_str) > 1000:
        raise InputError('length problem')
    # check each channel
    for channel in store['channels']:
        if check_user_in_channel(auth_user_id, channel):
            # check each message in each channel
            for message in channel['messages']:
                if query_str in message['message']:
                    result.append(message)
    # check each dm
    for dm in store['dms']:
        if check_user_in_dms(auth_user_id, dm):
            # check each message in each dm
            for message in dm['messages']:
                if query_str in message['message']:
                    result.append(message)
    return {
        'messages' : result
    }

# check whether the user in this channel
def check_user_in_channel(u_id, channel):
    for member in channel['all_members']:
        if member['u_id'] == u_id:
            return True
    return False

# check whether the user in this dm
def check_user_in_dms(u_id, dm):
    for member in dm['all_members']:
        if member['u_id'] == u_id:
            return True
    return False
