from src.data_store import data_store
from src.error import *
from src.other import *
from datetime import datetime, timezone

def channels_list_v1(token):
    '''list all the channels that the authorised user is a part of'''
    store = data_store.get()
    # search for the given token, if not, raise an AccessError
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)

    auth_user_id = input_dict['u_id']

    # create an empty list to store channels_list.
    channel_list = []
    for each_channel in store['channels']:
        for each_member in each_channel['all_members']:
            # search for any channel that the user is part of.
            if each_member['u_id'] == auth_user_id:
                # reset the channel_info dictionary to empty and then
                # append it to the list.
                channel_info = {}
                channel_info['channel_id'] = each_channel['channel_id']
                channel_info['name'] = each_channel['name']
                channel_list.append(channel_info)
    data_store.set(store)
    return {
        'channels': channel_list
    }

def channels_listall_v1(token):
    '''list all the channels whether the channel is public or private or not'''
    store = data_store.get()
    # search for the given user_id, if not, raise an AccessError
    check_valid_token(token, store['token'])
    
    channel_list = []
    # list out all the channels including private and public
    for each_channel in store['channels']:
        channel_info = {}
        channel_info['channel_id'] = each_channel['channel_id']
        channel_info['name'] = each_channel['name']
        channel_list.append(channel_info)
    data_store.set(store)
    return {
        'channels': channel_list
    }

def channels_create_v1(token, name, is_public):
    '''create a channel with specific keys in it'''
    store = data_store.get()
    # search for the given user_id, if not, raise an AccessError
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)
    auth_user_id = input_dict['u_id']
    # if entered name is less than 1 or greater than 20, raise an InputError.
    if not 1 <= len(name) <= 20:
        raise InputError("Invalid Channel Name")
    # set channel_id in asending order
    new_channel_id = len(store['channels']) + 1

    for each_user in store['users']:
        # check if the id exists or not
        if each_user['auth_user_id'] == auth_user_id:
            # create new time stamp
            stamp = {}
            stamp['num_channels_joined'] = each_user['channels_joined'][-1]['num_channels_joined'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['channels_joined'].append(stamp)
            # create an empty channel dictionary and add needed keys.
            new_channel = {}
            new_channel['name'] = name
            new_channel['channel_id'] = new_channel_id
            # set informations to the owner in a dictionary.
            new_owner = {}
            new_owner['u_id'] = auth_user_id
            new_owner['email'] = each_user['email']
            new_owner['name_first'] = each_user['name_first']
            new_owner['name_last'] = each_user['name_last']
            new_owner['handle_str'] = each_user['handle']
            new_owner['profile_img_url'] = each_user['profile_img_url']
            # append the owner to the owner list
            new_channel['owner_members'] = []
            new_channel['owner_members'].append(new_owner)
            # the only member will be the owner of the channel when first creating
            new_channel['all_members'] = []
            new_channel['all_members'].append(new_owner)
            # key of if_public status
            new_channel['is_public'] = is_public
            # set an empty list of messages
            new_channel['messages'] = []
            new_channel['stand_up'] = {}
            new_channel['stand_up']['is_active'] = False
            new_channel['stand_up']['message'] = []
            store['channels'].append(new_channel)
            data_store.set(store)
    # add time stamp
    stamp = {}
    stamp['num_channels_exist'] = store['channels_exist'][-1]['num_channels_exist'] + 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['channels_exist'].append(stamp)
    data_store.set(store)
    return {
        'channel_id': new_channel_id
    }
