from src.data_store import data_store
from src.error import *
from src.other import *
from src.notifications import *

# helper functions

def find_message_channel(message_id):
    store = data_store.get()
    for channel in store['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id']:
                return messages
    return False

def find_message_dm(message_id):
    store = data_store.get()
    for dm in store['dms']:
        for messages in dm['messages']:
            if message_id == messages['message_id']:
                return messages
    return False

def get_channel(message_id):
    store = data_store.get()
    channel_id = -1
    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                channel_id = channel['channel_id']
    return channel_id

def check_channel_owner(u_id, channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owner_members']:
                if u_id == owner['u_id']:
                    return True
    return False

def get_dm(message_id):
    store = data_store.get()
    dm_id = -1
    for dm in store['dms']:
        for message in dm['messages']:
            if message_id == message['message_id']:
                dm_id = dm['dm_id']
    return dm_id

def check_dm_owner(u_id, dm_id):
    store = data_store.get()
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            owner = dm['owner']
            if u_id == owner['u_id']:
                return True
    return False

# main code
def message_pin_v1(token, message_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)

    channel_message = find_message_channel(message_id)
    dm_message = find_message_dm(message_id)

    if channel_message == False and dm_message == False:
        raise InputError('Invalid message_id')
    if channel_message != False and channel_message['is_pinned'] == True:
        raise InputError('The message is already pinned')
    if dm_message != False and dm_message['is_pinned'] == True:
        raise InputError('The message is already pinned')

    if channel_message != False:
        channel_id = get_channel(message_id)
        if check_channel_owner(auth_user_id, channel_id) == True:
            channel_message['is_pinned'] = True
        else:
            raise AccessError('Authorised user does not have owner permissions')
    else:
        dm_id = get_dm(message_id)
        if check_dm_owner(auth_user_id, dm_id) == True:
            dm_message['is_pinned'] = True
        else:
            raise AccessError('Authorised user does not have owner permissions')
    data_store.set(store)
    return {}

def message_unpin_v1(token, message_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)

    channel_message = find_message_channel(message_id)
    dm_message = find_message_dm(message_id)

    if channel_message == False and dm_message == False:
        raise InputError('Invalid message_id')
    if channel_message != False and channel_message['is_pinned'] == False:
        raise InputError('The message is already pinned')
    if dm_message != False and dm_message['is_pinned'] == False:
        raise InputError('The message is already pinned')

    if channel_message != False:
        channel_id = get_channel(message_id)
        if check_channel_owner(auth_user_id, channel_id) == True:
            channel_message['is_pinned'] = False
        else:
            raise AccessError('Authorised user does not have owner permissions')
    else:
        dm_id = get_dm(message_id)
        if check_dm_owner(auth_user_id, dm_id) == True:
            dm_message['is_pinned'] = False
        else:
            raise AccessError('Authorised user does not have owner permissions')
    data_store.set(store)
    return {}