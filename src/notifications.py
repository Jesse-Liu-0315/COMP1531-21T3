from src.data_store import data_store
from src.error import *
from src.other import decode_jwt
from src.other import *

#given channel_id, check whether the channel existed in data
def check_valid_channel(channel_id):
    
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False
#given dm_id check whether dm_id is valid
def check_valid_dm(dm_id):
    
    store = data_store.get()
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            return dm
    return False

#given auth_user_id return the handle of that the auth_user
def user_handle(auth_user_id):
    store = data_store.get()
    the_handle = 0
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            the_handle = user['handle']
    return the_handle
        
#given the message_id and return the handle of the message sender
def message_handle(message_id):
    store = data_store.get()
    handle = 0
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                handle = user_handle(message['u_id'])
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                handle = user_handle(message['u_id'])
    return handle
        
#given the channel_id return the name of that channel
def channel_name(channel_id):
    store = data_store.get()
    the_channel_name = 0
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            the_channel_name = channel['name']
    return the_channel_name
#given the dm_id and return the name of that dm
def dm_name(dm_id):
    store = data_store.get()
    the_dm_name = 0
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            the_dm_name =  dm['name']
    return the_dm_name
#given the handle and return this handle's dictionary in all_notifications.
#If the handle doesn't have a dictionary, then create for the handle
def handle_notification(handle):
    store = data_store.get()
    for notification in store['all_notifications']:
        if notification['handle'] == handle:
            return notification
    notification = {
        'handle' : handle,
        'user_notification' : [],
    }
    store['all_notifications'].append(notification)
    return store['all_notifications'][-1]
#given handle and dm_id, check whether the handle is in the dm
def check_valid_handle_dm(handle, dm_id):
    target_dm = check_valid_dm(dm_id)
    for member in target_dm['all_members']:
        if member['handle_str'] == handle:
            return True
    return False
#given handle and channel_id, check whether the handle is in the channel
def check_valid_handle_channel(handle, channel_id):
    target_channel = check_valid_channel(channel_id)
    for member in target_channel['all_members']:
        if member['handle_str'] == handle:
            return True
    return False
#given message_id and return the channel_id the message in. If not in channel, return -1
def find_noti_channel(message_id):
    store = data_store.get()
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return channel['channel_id']
    return -1
#given message_id and return the dm_id the message in. If not in dm, return -1
def find_noti_dm(message_id):
    store = data_store.get()
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                return dm['dm_id']
    return -1
# given auth_user_id, message and message_id, 
# a user is tagged when a message contains the @ symbol, followed immediately by the user’s handle. 
# The end of the handle is signified by the end of the message, or a non-alphanumeric character. If the handle is invalid, 
# or the user is not a member of the channel or DM, no one is tagged.
def notification_tag(auth_user_id, message, message_id):
    channel_id = find_noti_channel(message_id)
    dm_id = find_noti_dm(message_id)
    #split every tagged user
    tagged_users = []
    splited_message = message.split()
    for message_part in splited_message:
        find_index = message_part.find('@')
        if find_index != -1 and message_part != '@':
            handle = message_part[find_index + 1:]
            tagged_users.append(handle)
    #if message length greater than 20, only use first 20
    if len(message) > 20:
        message = message[0:20]
    auth_handle = user_handle(auth_user_id)
    
    for tagged_user in tagged_users:
        #if channel_id == -1, then user tagged in dm
        if channel_id == -1:
            if check_valid_handle_dm(tagged_user, dm_id) == True:
                Dm_name = dm_name(dm_id)
                notification = {
                    'channel_id': channel_id,
                    'dm_id': dm_id,
                    'notification_message': f'{auth_handle} tagged you in {Dm_name}: {message}'
                }
                tagged_user_noti = handle_notification(tagged_user)
                tagged_user_noti['user_notification'].append(notification)
        #if dm_id == -1, then user tagged in channel
        if dm_id == -1:
            if check_valid_handle_channel(tagged_user, channel_id) == True:
                Channel_name = channel_name(channel_id)
                notification = {
                    'channel_id': channel_id,
                    'dm_id': dm_id,
                    'notification_message': f'{auth_handle} tagged you in {Channel_name}: {message}'
                }
                tagged_user_noti = handle_notification(tagged_user)
                tagged_user_noti['user_notification'].append(notification)

#given auth_user_id and message_id, if the auth_user react the message
#then the message sender will get a notification
def notification_react(auth_user_id, message_id):
    channel_id = find_noti_channel(message_id)
    dm_id = find_noti_dm(message_id)

    auth_handle = user_handle(auth_user_id)
    handle = message_handle(message_id)
    #if channel_id == -1, then the message reacted in dm
    if channel_id == -1:

        Dm_name = dm_name(dm_id)
        notification = {
            'channel_id': channel_id,
            'dm_id': dm_id,
            'notification_message': f'{auth_handle} reacted to your message in {Dm_name}'
        }
        user_noti = handle_notification(handle)
        user_noti['user_notification'].append(notification)
    #if dm_id == -1, then the message reacted in channel
    if dm_id == -1:
            
        Channel_name = channel_name(channel_id)
        notification = {
            'channel_id': channel_id,
            'dm_id': dm_id,
            'notification_message': f'{auth_handle} reacted to your message in {Channel_name}'
        }
        user_noti = handle_notification(handle)
        user_noti['user_notification'].append(notification)

#given auth_user_id dm_id and handle, if auth_user add user with the handle
#into the dm, then user with the handle will get a notification
def notification_add_dm(auth_user_id, dm_id, handle):
    
    auth_handle = user_handle(auth_user_id)

    Dm_name = dm_name(dm_id)
    notification = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': f'{auth_handle} added you to {Dm_name}'
    }
    user_noti = handle_notification(handle)
    user_noti['user_notification'].append(notification)

#given auth_user_id channel_id and handle, if auth_user add user with the handle
#into the channel, then user with the handle will get a notification
def notification_add_channel(auth_user_id, channel_id, handle):
    
    auth_handle = user_handle(auth_user_id)
    

    Channel_name = channel_name(channel_id)
    notification = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': f'{auth_handle} added you to {Channel_name}'
    }
    auth_user_noti = handle_notification(handle)
    auth_user_noti['user_notification'].append(notification) 

#given token, return the user's most recent 20 notifications, ordered from most recent to least recent.
def notifications_get_v1(token):
    
    store = data_store.get()
    check_valid_token(token, store['token'])

    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    
    handle = user_handle(auth_user_id)
    user_notification = handle_notification(handle)
    #return the most recent 20 notifications of the auth_user
    notifications = []
    if len(user_notification['user_notification']) <= 20:
        for each_notification in reversed(user_notification['user_notification']):
            notifications.append(each_notification)
    else:
        counter = 1
        while counter <= 20:
            notifications.append(user_notification['user_notification'][-counter])
            counter += 1
    
    data_store.set(store)
    return {'notifications' : notifications}



#given message_id and auth_user_id, check whether the auth_user_id
#is in the channel/dm the message is in. If True, return message else False
def check_valid_message_id(message_id, auth_user_id):
    store = data_store.get()
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                for member in channel['all_members']:
                    if member['u_id'] == auth_user_id:
                        return message

    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                for member in dm['all_members']:
                    if member['u_id'] == auth_user_id:
                        return message

    return False
#given auth_user_id and reacted_message, if the message already be reacted by
#that user, then return True, else False
def already_react(auth_user_id, reacted_message):
    
    for uid in reacted_message['reacts'][0]['u_ids']:
        if uid == auth_user_id:
            return True
    return False

#Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message.
def message_react_v1(token, message_id, react_id):

    store = data_store.get()
    check_valid_token(token, store['token'])

    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)
    react_id = int(react_id)

    reacted_message = check_valid_message_id(message_id, auth_user_id)
    #check whether the message_id is valid
    if reacted_message == False:
        raise InputError('invalid message_id')
    #check whether the reacted id is valid
    if react_id != 1:
        raise InputError('invalid react_id')
    #check whether the message has been reacted
    if already_react(auth_user_id, reacted_message):
        raise InputError('already react')
    #do react
    reacted_message['reacts'][0]['u_ids'].append(auth_user_id)
    notification_react(auth_user_id, message_id)
    data_store.set(store)
    return {}
#Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message.
def message_unreact_v1(token, message_id, react_id):
    
    store = data_store.get()
    check_valid_token(token, store['token'])

    token_data = decode_jwt(token)
    auth_user_id = token_data['u_id']
    message_id = int(message_id)
    react_id = int(react_id)

    unreacted_message = check_valid_message_id(message_id, auth_user_id)
    #check whether the message_id is valid
    if unreacted_message == False:
        raise InputError('invalid message_id')
    #check whether the reacted id is valid
    if react_id != 1:
        raise InputError('invalid react_id')
    #check whether the message has been reacted
    if already_react(auth_user_id, unreacted_message) == False:
        raise InputError('u did not react')
    #do unreact
    unreacted_message['reacts'][0]['u_ids'].remove(auth_user_id)
    notification_react(auth_user_id, message_id)
    data_store.set(store)
    return {}
