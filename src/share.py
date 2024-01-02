from src.data_store import data_store
from src.error import *
from src.other import *
from src.message import *


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    u_id = decode_jwt(token)['u_id']
    # find all channels and dms user joined
    user_channel_joined = find_target_user(u_id, store)[0]
    user_dm_joined = find_target_user(u_id, store)[1]
    # check if invalid channelid and dmid
    if check_valid_channel_share(channel_id, store) == False and check_valid_dm_share(dm_id, store) == False:
        raise InputError('Invalid Both Channel_id and Dm_id')
    # check if channelid and dmid both not -1
    if channel_id != -1 and dm_id != -1:
        raise InputError('Invalid Input_id')
    if channel_id not in user_channel_joined and dm_id not in user_dm_joined:
        raise AccessError('Not Join Target Channel or Dm')
    # check if message in not in joined channel or dm
    message_position_channel = get_target_message_position_channel(og_message_id, store)
    message_position_dm = get_target_message_position_dm(og_message_id, store)
    if message_position_channel not in user_channel_joined and message_position_dm not in user_dm_joined:
        raise InputError('Invalid Message_id')
    # length of message more than 1000
    if len(message) > 1000:
        raise InputError('Invalid Message')
    # find channel or dm which message is in
    if channel_id != -1:
        message_shared = find_message(og_message_id, store)['message']
        message_share_commit = create_message(message, message_shared)
        message_send_v1(token, channel_id, message_share_commit)
    else:
        message_shared = find_message(og_message_id, store)['message']
        message_share_commit = create_message(message, message_shared)
        message_senddm_v1(token, dm_id, message_share_commit)
    data_store.set(store)
    return {
        'shared_message_id': og_message_id
    }

# find all channels and dms user joined
def find_target_user(u_id, store):
    list_channel_joined = []
    list_dm_joined = []
    for each_channel in store['channels']:
        for each_member in each_channel['all_members']:
            if each_member['u_id'] == u_id:
                list_channel_joined.append(each_channel['channel_id'])
    for each_dm in store['dms']:
        for each_member in each_dm['all_members']:
            if each_member['u_id'] == u_id:
                list_dm_joined.append(each_dm['dm_id'])
    return [list_channel_joined, list_dm_joined]


def get_target_message_position_channel(og_message_id, store):
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == og_message_id:
                return channel['channel_id']
    return 0


def get_target_message_position_dm(og_message_id, store):
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == og_message_id:
                return dm['dm_id']
    return 0


def check_valid_channel_share(channel_id, store):
    for each_channel in store['channels']:
        if channel_id == each_channel['channel_id']:
            return True
    return False


def check_valid_dm_share(dm_id, store):
    for each_dm in store['dms']:
        if dm_id == each_dm['dm_id']:
            return True
    return False


def find_message(message_id, store):
    target_message = False
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                target_message = message
                break
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                target_message = message
                break
    return target_message

def create_message(message, message_shared):
    list_message = []
    list_message = message_shared.split('\n')
    counter = 1
    while counter < len(list_message):
        list_message[counter] = '\t' + list_message[counter]
        counter += 1
    message_shared = '\n'.join(list_message)
    message_return = f'''{message}

"""
{message_shared}
"""'''
    return message_return



