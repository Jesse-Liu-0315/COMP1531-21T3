from src.data_store import data_store
from src.error import *
from src.other import *
from datetime import datetime, timezone
from src.notifications import *

#This is the final version

#Helper functions:
def check_valid_start(start, target_channel):
    if start > len(target_channel['messages']) or start < 0:
        return False
    return True

#given channel_id, check whether the channel existed in data
'''def check_valid_channel(channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False'''
#given auth_user_id and target_channel, check whether the user 
#existed in the channel
def check_valid_member(auth_user_id, target_channel):
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            return True
    return False
#given u_id, check whether the user existed in data
def check_valid_user(u_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return user
    return False

#Given a channel with ID channel_id that the authorised user is a member of, provide basic details about the channel.
def channel_details_v2(token, channel_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    #check whether the target channel is valid
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    #check whether the auth user id valid
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('the authorised user is not a member of the channel')
    data_store.set(store)
    return {
        'name' : target_channel['name'],
        'is_public' : target_channel['is_public'],
        'owner_members' : target_channel['owner_members'],
        'all_members' : target_channel['all_members'],
    }

#Invites a user with ID u_id to join a channel with ID channel_id. Once invited, 
#the user is added to the channel immediately. In both public and private channels, 
#all members are able to invite users.
def channel_invite_v2(token, channel_id, u_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    invited_user = check_valid_user(u_id)
    #check whether the target channel is valid
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    #check whether the auth user is valid
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('the authorised user is not a member of the channel')
    #check whether the invited user is valid
    if invited_user == False:
        raise InputError('u_id does not refer to a valid user')
    #check whether the invited user is already in that channel
    if check_valid_member(u_id, target_channel) == True:
        raise InputError('a user who is already a member of the channel')
    #create and add time stamp
    for each_user in store['users']:
        if each_user['auth_user_id'] == u_id:
            stamp = {}
            stamp['num_channels_joined'] = each_user['channels_joined'][-1]['num_channels_joined'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['channels_joined'].append(stamp)
    #do channel invite
    user = {
        'u_id' : invited_user['auth_user_id'],
        'email' : invited_user['email'],
        'name_first' : invited_user['name_first'],
        'name_last' : invited_user['name_last'],
        'handle_str' : invited_user['handle'],
        'profile_img_url': store['users'][u_id-1]['profile_img_url']
    }
    target_channel['all_members'].append(user)
    notification_add_channel(auth_user_id, channel_id, invited_user['handle'])
    data_store.set(store)
    return {}

#Given a channel with ID channel_id that the authorised user is a member of, 
#return up to 50 messages between index "start" and "start + 50". 
#Message with index 0 is the most recent message in the channel. 
#This function returns a new index "end" which is the value of "start + 50", or, 
#if this function has returned the least recent messages in the channel, 
#returns -1 in "end" to indicate there are no more messages to load after this return.
def channel_messages_v2(token, channel_id, start):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    start = int(start)
    target_channel = check_valid_channel(channel_id)
    #check whether the target channel is valid
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    #check whether the auth user is in that channel
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('the authorised user is not a member of the channel')
    #check whether the start is at range
    if check_valid_start(start, target_channel) == False:
        raise InputError('start out of range')
    #do channel message for up to 50 messages
    mlist = []
    count = 0
    have_message = len(target_channel['messages']) - start
    counter = have_message
    while counter > 0:
        if count >= 50:
            break
        target_channel['messages'][counter - 1]['reacts'][0]['is_this_user_reacted']\
        = auth_user_id in target_channel['messages'][counter - 1]['reacts'][0]['u_ids']
        mlist.append(target_channel['messages'][counter - 1])
        counter -= 1
        count += 1
    if count < 50:
        end = -1
    else:
        end = start + 50
    data_store.set(store)
    return {
        'messages': mlist,
        'start': start,
        'end': end,
    }

#Given a channel_id of a channel that the authorised user can join, adds them to that channel.
def channel_join_v2(token, channel_id):
    store = data_store.get()
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    joined_user = check_valid_user(auth_user_id)
    #check whether the target channel is valid
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    #check whether the auth user has permission to join that channel
    if (target_channel['is_public'] == 0) and (joined_user['permission_id'] == 2):
        raise AccessError('channel_id refers to a channel that is private and the authorised user is not a permission_id')
    #check whether the auth user is a member of that channel
    if check_valid_member(auth_user_id, target_channel) == True:
        raise InputError('a user who is already a member of the channel')
    #create and add time stamp
    for each_user in store['users']:
        if each_user['auth_user_id'] == auth_user_id:
            stamp = {}
            stamp['num_channels_joined'] = each_user['channels_joined'][-1]['num_channels_joined'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['channels_joined'].append(stamp)
    #do channel join
    user = {
        'u_id' : joined_user['auth_user_id'],
        'emaiil' : joined_user['email'],
        'name_first' : joined_user['name_first'],
        'name_last' : joined_user['name_last'],
        'handle_str' : joined_user['handle'],
        'profile_img_url': store['users'][auth_user_id-1]['profile_img_url']
    }

    target_channel['all_members'].append(user)
    data_store.set(store)
    return {}

def channel_leave_v1(token, channel_id):
    store = data_store.get()
    # Check the token valid or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    # get the token_id
    auth_user_id = token_data['u_id']
    # get the channel_id
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    # get the position of channel
    position = 0
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            break
        position += 1
    # error
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    if check_valid_member(auth_user_id, target_channel) == False:
        raise AccessError('a user who is not a member of the channel')
    # remove the data in owner_member
    for member in target_channel['owner_members']:
        if member['u_id'] == auth_user_id:
            store['channels'][position]['owner_members'].remove(member)
    # remove the data in all_member
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            store['channels'][position]['all_members'].remove(member)
    for each_user in store['users']:
        if each_user['auth_user_id'] == auth_user_id:
            stamp = {}
            stamp['num_channels_joined'] = each_user['channels_joined'][-1]['num_channels_joined'] - 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['channels_joined'].append(stamp)
    data_store.set(store)
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    store = data_store.get()
    # Check the token valid or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    # get the token_id
    auth_user_id = token_data['u_id']
    # get the channel_id
    channel_id = int(channel_id)
    target_channel = check_valid_channel(channel_id)
    u_id = int(u_id)
    # error
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    add_owner = check_valid_user(u_id)
    # consider premission id    
    flag = 0
    for user in target_channel['all_members']:
        if auth_user_id == user['u_id'] and check_valid_user(auth_user_id)['permission_id'] == 1 :
            flag += 1
    for user in target_channel['owner_members']:
        if auth_user_id == user['u_id']:
            flag += 1
    if flag == 0:
        raise AccessError('authorised user does not have owner permissions in the channel')
    if add_owner == False:
        raise InputError('u_id does not refer to a valid user')
    flag = 0
    for user in target_channel['all_members']:
        if u_id == user['u_id']:
            flag += 1
    if flag == 0:
        raise InputError('u_id refers to a user who is not a member of the channel')
    for user in target_channel['owner_members']:
        if u_id == user['u_id']:
            raise InputError('u_id refers to a user who is already an owner of the channel')
    # add data in owner_member
    user = {
        "u_id" : u_id,
        "email" : add_owner['email'],
        "name_first" : add_owner['name_first'],
        "name_last" : add_owner['name_last'],
        "handle_str" : add_owner['handle'],
        'profile_img_url': store['users'][u_id-1]['profile_img_url']
    }
    target_channel['owner_members'].append(user)
    data_store.set(store)
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    store = data_store.get()
    # Check the token valid or not
    check_valid_token(token, store['token'])
    token_data = decode_jwt(token)
    # get the token_id
    auth_user_id = token_data['u_id']
    # get the channel_id
    channel_id = int(channel_id)
    # get u_id
    u_id = int(u_id)
    target_channel = check_valid_channel(channel_id)
    # find the position of channel
    position = 0
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            break
        position += 1
    # error
    if target_channel == False:
        raise InputError('channel_id does not refer to a valid channel')
    remove_owner = check_valid_user(u_id)
    # consider premission id   
    flag = 0
    for user in target_channel['all_members']:
        if auth_user_id == user['u_id'] and check_valid_user(auth_user_id)['permission_id'] == 1 :
            flag += 1
    for user in target_channel['owner_members']:
        if auth_user_id == user['u_id']:
            flag += 1
    if flag == 0:
        raise AccessError('authorised user does not have owner permissions in the channel')
    if remove_owner == False:
        raise InputError('u_id does not refer to a valid user')
    flag = 0
    for user in target_channel['owner_members']:
        if u_id == user['u_id']:
            flag += 1
    if flag == 0:
        raise InputError('u_id refers to a user who is not an owner of the channel')
    if len(target_channel['owner_members']) == 1:
        raise InputError('u_id refers to a user who is currently the only owner of the channel')
    # remove data in owner_members
    for member in target_channel['owner_members']:
        if member['u_id'] == u_id:
            store['channels'][position]['owner_members'].remove(member)
            data_store.set(store)
    return {}
