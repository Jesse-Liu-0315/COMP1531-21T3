from src.data_store import data_store
from src.error import *
from src.other import *
from src.notifications import *
from threading import Timer
from datetime import datetime, timezone


#given start and target_dm, check whether the start is valid
def check_valid_start_dm(start, target_dm):
    if start > len(target_dm['messages']) or start < 0:
        return False
    return True

#given auth_user_id and target_channel, check whether the user 
#existed in the channel
def check_valid_member(auth_user_id, target_channel):
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            return True
    return False

#given auth_user_id and target_dm, check whether the
#auth_user_id is in the target_dm 
def check_valid_member_dm(auth_user_id, target_dm):
    for member in target_dm['all_members']:
        if member['u_id'] == auth_user_id:
            return True
    return False

#generate a new message_id and should be distinct and
#do not use the previous message_id removed
def create_message_id():
    store = data_store.get()
    message_count = 0
    for channel in store['channels']:
        for message in channel['messages']:
            message = message
            message_count = message_count + 1
    for dm in store['dms']:
        for message in dm['messages']:
            message_count = message_count + 1
    message_count = message_count + 1
    message_count = message_count + len(store['message_id_removed'])
    return message_count

#if the_message is send by the auth_user_id, then return True
#if the auth_user_id is the owner of the channel/dm or 
#the global_owner with permission_id 1, then return True.
#if none of True, return False
def check_none_of_true(message_id, auth_user_id, the_message):
    if the_message['u_id'] == auth_user_id:
        return True
    store = data_store.get()
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                for owner in channel['owner_members']:
                    if owner['u_id'] == auth_user_id:
                        return True
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            if user['permission_id'] == 1:
                return True
    return False

# Send a message from the authorised user to the channel specified by channel_id. 
# Each message should have its own unique ID, i.e. no messages should share an ID with another message, 
# even if that other message is in a different channel.
def message_send_v1(token, channel_id, message):
    global send_message_return_message_id
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    #check whether the channel id is valid
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    #check whether the auth user is a member of that channel
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('the authorised user is not a member of the channel')
    #check the length of that message
    if len(message) < 1 or len(message) > 1000:
        raise InputError('length problem')
    #do message create and send
    message_id = create_message_id()
    message = {
        "message_id" : message_id,
        "u_id" : auth_user_id,
        "message" : message,
        "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
        "reacts" : [
            {
                "react_id" : 1,
                "u_ids" : [],
                "is_this_user_reacted" : False,
            },
        ],
        "is_pinned" : False,
    }
    target_channel['messages'].append(message)
    #create time stamp
    for each_user in store['users']:
        if each_user['auth_user_id'] == auth_user_id:
            stamp = {}
            stamp['num_messages_sent'] = each_user['messages_sent'][-1]['num_messages_sent'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['messages_sent'].append(stamp)
    # add time stamp
    stamp = {}
    stamp['num_messages_exist'] = store['messages_exist'][-1]['num_messages_exist'] + 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['messages_exist'].append(stamp)
    
    notification_tag(auth_user_id, message['message'], message_id)
    data_store.set(store)
    send_message_return_message_id = message_id
    return {
        'message_id' : message_id
    }

#Given a message, update its text with new text. If the new message is an empty string, the message is deleted.
def message_edit_v1(token, message_id, message):
    store = data_store.get()
    check_valid_token(token, store['token'])
    #if the length of that message is 0, remove that message
    if len(message) == 0:
        message_remove_v1(token, message_id)
        return {}
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)
    edited_message = check_valid_message_id(message_id, auth_user_id)
    #check whether the length of that message is valid
    if len(message) > 1000:
        raise InputError('length problem')
    #check whether the message id of that message is valid
    if edited_message == False:
        raise InputError('invalid message_id')
    #check whether the auth user has permission to edit that message
    if check_none_of_true(message_id, auth_user_id, edited_message) == False:
        raise AccessError('none of true')
    #do message edit
    edited_message['message'] = message
    notification_tag(auth_user_id, message, message_id)
    data_store.set(store)
    return {}
    
#Given a message_id for a message, this message is removed from the channel/DM
def message_remove_v1(token, message_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)
    removed_message = check_valid_message_id(message_id, auth_user_id)
    #check whether the message is valid
    if removed_message == False:
        raise InputError('invalid message')
    #check whether the auth user has permission to remove that message
    if check_none_of_true(message_id, auth_user_id, removed_message) == False:
        raise AccessError('none of true')
    #do message remove
    store = data_store.get()
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                channel['messages'].remove(message)
                store['message_id_removed'].append(message)
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm['messages'].remove(message)
                store['message_id_removed'].append(message)
    # add time stamp
    stamp = {}
    stamp['num_messages_exist'] = store['messages_exist'][-1]['num_messages_exist'] - 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['messages_exist'].append(stamp)
    data_store.set(store)
    return {}

#Send a message from authorised_user to the DM specified by dm_id.
#Each message should have it's own unique ID, i.e. no messages should share an ID with another message,
#even if that other message is in a different channel or DM.
def message_senddm_v1(token, dm_id, message):
    global send_dm_message_return_dm_id
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    dm_id = int(dm_id)
    target_dm = check_valid_dm(dm_id)
    #check whether the dm is valid
    if target_dm == False:
        raise InputError('dm_id does not refer to a valid dm')
    #check whether the auth user is a member of that dm
    if check_valid_member_dm(auth_user_id, target_dm) == False:
        raise AccessError('the authorised user is not a member of the dm')
    #check whether the length of the message is valid
    if len(message) < 1 or len(message) > 1000:
        raise InputError('length problem')
    #do message senddm
    message_id = create_message_id()
    
    message = {
        "message_id" : message_id,
        "u_id" : auth_user_id,
        "message" : message,
        "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
        "reacts" : [
            {
                "react_id" : 1,
                "u_ids" : [],
                "is_this_user_reacted" : False,
            },
        ],
        "is_pinned" : False,
    }
    #create time stamp
    for each_user in store['users']:
        if each_user['auth_user_id'] == auth_user_id:
            stamp = {}
            stamp['num_messages_sent'] = each_user['messages_sent'][-1]['num_messages_sent'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['messages_sent'].append(stamp)
    # add time stamp
    stamp = {}
    stamp['num_messages_exist'] = store['messages_exist'][-1]['num_messages_exist'] + 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['messages_exist'].append(stamp)
    target_dm['messages'].append(message)
    send_dm_message_return_dm_id = message_id
    
    notification_tag(auth_user_id, message['message'], message_id)
    data_store.set(store)
    return {'message_id' : message_id}

#Given a DM with ID dm_id that the authorised user is a member of, 
#return up to 50 messages between index "start" and "start + 50". 
#Message with index 0 is the most recent message in the DM. 
#This function returns a new index "end" which is the value of "start + 50", or, 
#if this function has returned the least recent messages in the DM, 
#returns -1 in "end" to indicate there are no more messages to load after this return.

def dm_messages_v1(token, dm_id, start):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    dm_id = int(dm_id)
    start = int(start)
    target_dm = check_valid_dm(dm_id)
    #check whether the dm is valid
    if target_dm == False:
        raise InputError('dm_id does not refer to a valid dm')
    #check whether the auth user is a member of that dm
    if check_valid_member_dm(auth_user_id, target_dm) == False:
        raise AccessError('the authorised user is not a member of the dm')
    #check whether the start is at range
    if check_valid_start_dm(start, target_dm) == False:
        raise InputError('start out of range')
    #do dm message for up to 50 messages
    mlist = []
    count = 0
    have_message = len(target_dm['messages']) - start
    counter = have_message
    while counter > 0:
        if count >= 50:
            break
        target_dm['messages'][counter - 1]['reacts'][0]['is_this_user_reacted']\
        = auth_user_id in target_dm['messages'][counter - 1]['reacts'][0]['u_ids']
        mlist.append(target_dm['messages'][counter - 1])
        counter -= 1
        count += 1

    if count < 50:
        end = -1
    #elif count >= 50:
    else:
        end = start + 50
    data_store.set(store)
    return {
        'messages': mlist,
        'start': start,
        'end': end,
    }


def message_sendlater_v1(token, channel_id, message, time_sent):
    store = data_store.get()
    # check whether the token is vaild or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    time_sent = int(time_sent)
    # check channel_id does not refer to a valid channel
    target_channel = check_valid_channel(channel_id)
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    # check channel_id is valid and the authorised user is not a member of the channel they are trying to post to
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('the authorised user is not a member of the channel')
    # check whether length of message satisfy the requirement
    if len(message) < 1 or len(message) > 1000:
        raise InputError('length problem')
    # get present time in integer and the second user want to send_late
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    late_length = time_sent - present_time
    # check whether the time user selected is in the past
    if late_length < 0:
        raise InputError('the time is in the past')
    # wait until get the return value
    timer = Timer(late_length, message_send_v1, [token, channel_id, message])
    timer.start()
    timer.join()
    data_store.set(store)
    return {'message_id' : send_message_return_message_id}

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    store = data_store.get()
    # check whether the token is vaild or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    dm_id = int(dm_id)
    time_sent = int(time_sent)
    # check channel_id does not refer to a valid dm
    target_dm = check_valid_dm(dm_id)
    if target_dm == False:
        raise InputError('dm_id does not refer to a valid dm')
    # dm_id is valid and the authorised user is not a member of the dm they are trying to post to
    if check_valid_member_dm(auth_user_id, target_dm) == False:
        raise AccessError('the authorised user is not a member of the dm')
    # check whether length of message satisfy the requirement
    if len(message) < 1 or len(message) > 1000:
        raise InputError('length problem')
    # get present time in integer and the second user want to send_late
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    late_length = time_sent - present_time
    # check whether the time user selected is in the past
    if late_length < 0:
        raise InputError('the time is in the past')
    # wait until get the return value
    timer = Timer(late_length, message_senddm_v1, [token, dm_id, message])
    timer.start()
    timer.join()
    data_store.set(store)
    return {'message_id' : send_message_return_message_id}
