from src.data_store import data_store
from src.error import *
from src.other import *
from datetime import datetime, timezone
from src.notifications import *

# create a new directed message with specific keys
def dm_create_v1(token, u_ids):
    store = data_store.get()
    #check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    # get the input dict when encoding
    input_dict = decode_jwt(token)
    input_id = input_dict['u_id']

    counter = 0
    new_dm = {}
    user_name_list = []
    all_member_list = []
    # search for the u_ids that can be added to the dm
    for each_user in store['users']:
        for each_directed_user_id in u_ids:
            if each_directed_user_id == each_user['auth_user_id']:
                new_member = {}
                # create new time stamp
                stamp = {}
                stamp['num_dms_joined'] = each_user['dms_joined'][-1]['num_dms_joined'] + 1
                stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
                each_user['dms_joined'].append(stamp)
                # append all users' handle_str to the list
                new_member['u_id'] = each_user['auth_user_id']
                new_member['email'] = each_user['email']
                new_member['name_first'] = each_user['name_first']
                new_member['name_last'] = each_user['name_last']
                new_member['handle_str'] = each_user['handle']
                new_member['profile_img_url'] = each_user['profile_img_url']
                user_name_list.append(each_user['handle'])
                all_member_list.append(new_member)
                counter += 1
    # if didn't find all users that have passed in
    if counter != len(u_ids):
        raise InputError('User requested is not valid!')
    dm_owner = {}
    for each_user in store['users']:
        if each_user['auth_user_id'] == input_id:
            # create new time stamp
            stamp = {}
            stamp['num_dms_joined'] = each_user['dms_joined'][-1]['num_dms_joined'] + 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['dms_joined'].append(stamp)
            # add owner's info
            user_name_list.append(each_user['handle'])
            dm_owner['u_id'] = input_id
            dm_owner['handle_str'] = each_user['handle']
            dm_owner['email'] = each_user['email']
            dm_owner['name_first'] = each_user['name_first']
            dm_owner['name_last'] = each_user['name_last']
            dm_owner['profile_img_url'] = each_user['profile_img_url']
    new_dm_id = len(store['dms']) + 1
    # form the structure of a new dm
    new_dm['dm_id'] = new_dm_id
    user_name_list.sort()
    dm_name = ', '
    new_dm['name'] = dm_name.join(user_name_list)
    new_dm['owner'] = dm_owner
    all_member_list.insert(0, dm_owner)
    new_dm['all_members'] = all_member_list
    new_dm['messages'] = []
    store['dms'].append(new_dm)
    # add time stamp
    stamp = {}
    stamp['num_dms_exist'] = store['dms_exist'][-1]['num_dms_exist'] + 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['dms_exist'].append(stamp)
    
    counter = 1
    while counter < len(new_dm['all_members']):
        notification_add_dm(input_id, new_dm_id, new_dm['all_members'][counter]['handle_str'])
        counter += 1
        
    data_store.set(store)
    return {
        'dm_id': new_dm_id
    }

# list all the dms that the authorised user is part of
def dm_list_v1(token):
    store = data_store.get()
    # check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    # get the input dict when encoding
    input_dict = decode_jwt(token)
    input_id = input_dict['u_id']   
    dm_list = []
    # get all the dms that user is a part of
    for each_dm in store['dms']:
        dm_info = {}
        for each_member in each_dm['all_members']:
            if input_id == each_member['u_id']:
                dm_info['dm_id'] = each_dm['dm_id']
                dm_info['name'] = each_dm['name']
                dm_list.append(dm_info)
    return {
        'dms': dm_list
    }

# remove a dm by the creator
def dm_remove_v1(token, dm_id):
    store = data_store.get()
    # check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    # get the input dict when encoding
    input_dict = decode_jwt(token)
    input_id = input_dict['u_id']
    # set the configeration value of checking 
    dm_id_counter = 1
    dm_owner_counter = 1
    # check if the passed in user is the creator of the dm
    for each_dm in store['dms']:
        # check if the dm_id is valid
        if each_dm['dm_id'] == dm_id:
            dm_id_counter = 0
            if each_dm['owner']['u_id'] == input_id:
                dm_owner_counter = 0
    if dm_id_counter == 1:
        raise InputError('Dm_id does not refer to a valid DM')
    if dm_owner_counter == 1:
        raise AccessError('User is not the creator of the DM')
    # search for the right dm
    for each_dm in store['dms']:
        if each_dm['dm_id'] == dm_id:
            for each_member in each_dm['all_members']:
                for each_user in store['users']:
                    if each_user['auth_user_id'] == each_member['u_id']:
                        stamp = {}
                        stamp['num_dms_joined'] = each_user['dms_joined'][-1]['num_dms_joined'] - 1
                        stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
                        each_user['dms_joined'].append(stamp)
        store['dms'].remove(each_dm)
    # add time stamp
    stamp = {}
    stamp['num_dms_exist'] = store['dms_exist'][-1]['num_dms_exist'] - 1
    stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    store['dms_exist'].append(stamp)
    data_store.set(store)
    return {}

# leave a target dm
def dm_leave_v1(token, dm_id):
    store = data_store.get()
    # Check the token valid or not
    check_valid_token(token, store['token'])
    input_dict = decode_jwt(token)
    input_id = input_dict['u_id']
    flag_input = 0
    flag_acc = 0
    position = 0
    # find the position of dm_id and remove data from all_members
    for each_dm in store['dms']:
        if each_dm['dm_id'] == dm_id:
            flag_input += 1
            for member in each_dm['all_members']:
                if member['u_id'] == input_id:
                    flag_acc += 1
                    store['dms'][position]['all_members'].remove(member)
        position = position + 1
    # error checking
    if flag_input == 0:
        raise InputError('Dm_id does not refer to a valid DM')
    if flag_acc == 0:
        raise AccessError('User is not in the DM')
    # add time stamp
    for each_user in store['users']:
        if each_user['auth_user_id'] == input_id:
            stamp = {}
            stamp['num_dms_joined'] = each_user['dms_joined'][-1]['num_dms_joined'] - 1
            stamp['time_stamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            each_user['dms_joined'].append(stamp)
    data_store.set(store)
    return {}

# list target dm's detail
def dm_details_v1(token, dm_id):
    store = data_store.get()
    # check if the passed token is valid or not, if not, raise an accesserror
    check_valid_token(token, store['token'])
    # get the input dict when encoding
    input_dict = decode_jwt(token)
    input_id = input_dict['u_id']
    dm_id = int(dm_id)
    # set the configeration value of checking 
    dm_id_counter = 1
    dm_member_counter = 1
    for each_dm in store['dms']:
        # check if the dm_id is valid
        if each_dm['dm_id'] == dm_id:
            dm_id_counter = 0    
            for each_member in each_dm['all_members']:
                # check if the passed in user is the creator of the dm
                if each_member['u_id'] == input_id:
                    dm_member_counter = 0
    # error checking
    if dm_id_counter == 1:
        raise InputError('Dm_id does not refer to a valid DM')                
    if dm_member_counter == 1:
        raise AccessError('User is not a member of the DM')
    # add dm details
    detail_info = {}
    for each_dm in store['dms']:
        if each_dm['dm_id'] == dm_id:
            for each_member in each_dm['all_members']:
                if input_id == each_member['u_id']:
                    detail_info['name'] = each_dm['name']
                    detail_info['members'] = each_dm['all_members']
    return detail_info
