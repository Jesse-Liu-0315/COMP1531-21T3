from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import *
from src.message import message_send_v1
from threading import Timer
from datetime import datetime, timezone
import math


def channel_check(store, auth_user_id, channel_id):
    channel_id_check = 0
    channel_standup_status = 0
    member_in_channel_check = 0
    for each_channel in store['channels']:
        if each_channel['channel_id'] == channel_id:
            channel_id_check = 1
            if each_channel['stand_up']['is_active'] == True:
                channel_standup_status = 1
            # if the standup status is False
            else: 
                channel_standup_status = 2
            for each_member in each_channel['all_members']:
                if each_member['u_id'] == auth_user_id:
                    member_in_channel_check = 1
    # return a dictionary for all the checks
    return {
        'id_check': channel_id_check,
        'status_check': channel_standup_status,
        'member_check': member_in_channel_check 
    }


def standup_start_v1(token, channel_id, length):
    store = data_store.get()
    #check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    result = channel_check(store, auth_user_id, channel_id) 
    # channel_id is valid and the authorised user is not a member of the channel
    if result['id_check'] == 1 and result['member_check'] == 0:
        raise AccessError('The authorised user is not a member of the channel.')
    # Channel_id does not refer to a valid channel
    if result['id_check'] == 0:
        raise InputError('Channel_id does not refer to a valid channel.')
    # Entered negative length of seconds
    if length <= 0:
        raise InputError('Entered negative length of seconds.')
    # an active standup is currently running in the channel
    if result['status_check'] == 1:
        raise InputError("The standup is currently active in the channel")
    # add key status of the channel
    length = math.floor(length)
    time_stamp_finished = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + length    
    for each_channel in store['channels']:
        if each_channel['channel_id'] == channel_id:
            each_channel['stand_up']['is_active'] = True
            each_channel['stand_up']['message'] = []
            each_channel['stand_up']['length'] = length
            each_channel['stand_up']['time_finish'] = time_stamp_finished
    # countdown the length of seconds
    timer = Timer(length, send_packaged_message, [store, token, channel_id])
    timer.start()           
    data_store.set(store)
    return {
        'time_finish': int(time_stamp_finished)
    }


def standup_active_v1(token, channel_id):
    store = data_store.get()
    #check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    channel_id = int(channel_id)
    result = channel_check(store, auth_user_id, channel_id)         
    if result['id_check'] == 0:
        raise InputError('Channel_id does not refer to a valid channel.')
    if result['id_check'] == 1 and result['member_check'] == 0:
        raise AccessError('The authorised user is not a member of the channel.')

    for each_channel in store['channels']:
        if each_channel['channel_id'] == channel_id:
            standup_status = each_channel['stand_up']['is_active']
            if standup_status == False:
                finished_time = None
            else: finished_time = each_channel['stand_up']['time_finish']
    data_store.set(store)
    return {
        'is_active': standup_status,
        'time_finish': finished_time
    }


def standup_send_v1(token, channel_id, message):
    store = data_store.get()
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    for each_channel in store['channels']:
        for each_member in each_channel['all_members']:
            if each_member['u_id'] == auth_user_id:
                # turn the message to a grouped format
                combined_message = each_member['handle_str'] + ':' + ' ' + message
                each_channel['stand_up']['message'].append(combined_message)
    result = channel_check(store, auth_user_id, channel_id)         
    # The authorised user is not a member of the channel
    if result['id_check'] == 1 and result['member_check'] == 0:
        raise AccessError('The authorised user is not a member of the channel.')
    # Channel_id does not refer to a valid channel
    if result['id_check'] == 0:
        raise InputError('Channel_id does not refer to a valid channel.')
    # long message
    if len(message) > 1000:
        raise InputError('Too long message!')
    # The standup is not active in the channel
    if result['status_check'] == 2:
        raise InputError("The standup is not active in the channel")
    data_store.set(store)
    return {}


def send_packaged_message(store, token, channel_id):
    for each_channel in store['channels']:
        if each_channel['channel_id'] == channel_id:
            # standup is finished and make the status False
            each_channel['stand_up']['is_active'] = False 
            packaged_message = each_channel['stand_up']['message']  
            packaged_message = '\n'.join(packaged_message)  
            message_send_v1(token, channel_id, packaged_message)
