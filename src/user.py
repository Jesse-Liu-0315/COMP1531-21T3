import requests
import urllib.request
import urllib.error
from PIL import Image
from src.data_store import *
from src.error import *
from src.other import *
from src.auth import *

# users_all function should return all users' information
# except 'Removed user'
def users_all_v1(token):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # create a new list of users
    users = []
    for user in store['users']:
        if user['removed'] == False:
            users.append({'u_id': user['auth_user_id'],
                          'email': user['email'],
                          'name_first': user['name_first'],
                          'name_last': user['name_last'],
                          'handle_str': user['handle'],
                          'profile_img_url': user['profile_img_url']
            })
    return {
        'users': users
    }

# user_profile should return user's profile even been removed
def user_profile_v1(token, u_id):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # cheak whether valid u_id
    judge = 0
    u_id = int(u_id)
    for user_1 in store['users']:
        if u_id == user_1['auth_user_id']:
            judge += 1
    if judge == 0:
        raise InputError("Invalid U_id")
    # create a new list of target user
    user_target = {}
    for user_2 in store['users']:
        if user_2['auth_user_id'] == u_id:
            user_target['u_id'] = user_2['auth_user_id']
            user_target['email'] = user_2['email']
            user_target['name_first'] = user_2['name_first']
            user_target['name_last'] = user_2['name_last']
            user_target['handle_str'] = user_2['handle']
            user_target['profile_img_url'] = user_2['profile_img_url']
    return {
        'user': user_target
    }

# reset user's name
def user_profile_setname_v1(token, name_first, name_last):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # check name is valid or not
    check_valid_name(name_first, name_last)
    # update name
    token_decoded = decode_jwt(token)
    for user in store['users']:
        if token_decoded['u_id'] == user['auth_user_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last
    for channel in store['channels']:
        for each_owner in channel['owner_members']:
            if token_decoded['u_id'] == each_owner['u_id']:
                each_owner['name_first'] = name_first
                each_owner['name_last'] = name_last
        for each_member in channel['all_members']:
            if token_decoded['u_id'] == each_member['u_id']:
                each_member['name_first'] = name_first
                each_member['name_last'] = name_last
    for dm in store['dms']:
        for each_member in dm['all_members']:
            if token_decoded['u_id'] == each_member['u_id']:
                each_member['name_first'] = name_first
                each_member['name_last'] = name_last
        if dm['owner']['u_id'] == token_decoded['u_id']:
            dm['owner']['name_first'] = name_first
            dm['owner']['name_last'] = name_last
    data_store.set(store)
    return {}

# reset user's email
def user_profile_setemail_v1(token, email):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # check email is valid or not
    check_valid_email(email)
    # update email
    token_decoded = decode_jwt(token)
    for user in store['users']:
        if token_decoded['u_id'] == user['auth_user_id']:
            user['email'] = email
    for dm in store['dms']:
        for each_member in dm['all_members']:
            if token_decoded['u_id'] == each_member['u_id']:
                each_member['email'] = email
    data_store.set(store)
    return {}

# reset user's handle
def user_profile_sethandle_v1(token, handle_str):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # check handle is valid or not
    if not 3 <= len(handle_str) <= 20:
        raise InputError("Invalid handle_str")
    if handle_str.isalnum() == False:
        raise InputError("Invalid handle_str")
    judge = 0
    for user in store['users']:
        if handle_str == user['handle']:
            judge += 1
    if judge != 0:
        raise InputError("Used Handle_str")
    # update handle
    token_decoded = decode_jwt(token)
    for user in store['users']:
        if token_decoded['u_id'] == user['auth_user_id']:
            user['handle'] = handle_str
    for dm in store['dms']:
        for each_member in dm['all_members']:
            if token_decoded['u_id'] == each_member['u_id']:
                each_member['handle_str'] = handle_str
    data_store.set(store)
    return {}

# upload photo to a user's profile
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # check for valid image url
    try:
        image_status = requests.get(img_url)
    except requests.ConnectionError as error:
        raise InputError("Input Not A URL") from error
    if image_status.status_code != 200:
        raise InputError("Invalid Img_url")
    # check for valid input coordinates
    if x_end < x_start or y_end < y_start:
        raise InputError('Invalid Coordinates')
    # search for target user and update his photo
    target_user_id = decode_jwt(token)['u_id']
    new_photo_path_local = ''
    new_photo_path_local = each_user_image_address_local + str(target_user_id) + '.jpg'
    # download image
    urllib.request.urlretrieve(img_url, new_photo_path_local)
    # check for valid image type
    img_data = Image.open(new_photo_path_local)
    if img_data.format != 'JPEG':
        raise InputError("Image uploaded is not a JPG.")
    # get the width and height of image
    image_width = img_data.width
    image_height = img_data.height
    if x_start < 0 or y_start < 0 or x_end > image_width or y_end > image_height:
        raise InputError('Invalid Coordinates')
    crop_photo(new_photo_path_local, x_start, y_start, x_end, y_end)
    # store new cropped photo in folder
    # update in users
    store['users'][target_user_id-1]['profile_img_url'] = each_user_image_address_http + str(target_user_id) + '.jpg'
    # update in channels
    for each_channel in store['channels']:
        for each_owner in each_channel['owner_members']:
            if target_user_id == each_owner['u_id']:
                each_owner['profile_img_url'] = each_user_image_address_http + str(target_user_id) + '.jpg'
        for each_member in each_channel['all_members']:
            if target_user_id == each_member['u_id']:
                each_member['profile_img_url'] = each_user_image_address_http + str(target_user_id) + '.jpg'
    # update in dms
    for each_dm in store['dms']:
        for each_member in each_dm['all_members']:
            if target_user_id == each_member['u_id']:
                each_member['profile_img_url'] = each_user_image_address_http + str(target_user_id) + '.jpg'
    data_store.set(store)
    return {}

# crop image
def crop_photo(new_photo_path, x_start, y_start, x_end, y_end):
    imageObject = Image.open(new_photo_path)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(new_photo_path)
    return

# display user's stats
def user_stats_v1(token):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # search for channels and dms and messages user related
    user_id = decode_jwt(token)['u_id']
    num_channels_joined = get_num_channels_joined(user_id, store['users'])
    num_dms_joined = get_num_dms_joined(user_id, store['users'])
    messages_sent = get_num_messages_sent(user_id, store['users'])
    # search for channels and dms and messages existed
    num_channels = get_num_channels(store)
    num_dms = get_num_dms(store)
    num_msgs = get_num_messages(store)
    # calculate the result
    user_stats = {}
    user_stats['channels_joined'] = store['users'][user_id-1]['channels_joined']
    user_stats['dms_joined'] = store['users'][user_id-1]['dms_joined']
    user_stats['messages_sent'] = store['users'][user_id-1]['messages_sent']
    list_user_joined = [num_channels_joined, num_dms_joined, messages_sent]
    list_exist = [num_channels, num_dms, num_msgs]
    if sum(list_exist) == 0:
        user_stats['involvement_rate'] = 0
    else:
        user_stats['involvement_rate'] = min(sum(list_user_joined)/sum(list_exist), 1)

    return {
        'user_stats': user_stats
    }

# display all users' stats
def users_stats_v1(token):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    # create a empty dictionary
    workspace_stats = {}
    workspace_stats['channels_exist'] = store['channels_exist']
    workspace_stats['dms_exist'] = store['dms_exist']
    workspace_stats['messages_exist'] = store['messages_exist']
    num_users_who_have_joined_at_least_one_channel_or_dm = get_rate(store)
    workspace_stats['utilization_rate'] = num_users_who_have_joined_at_least_one_channel_or_dm/len(store['users'])

    return {
        'workspace_stats': workspace_stats
    }

# count the number of channel user joined
def get_num_channels_joined(u_id, users):
    num_channels_joined = 0
    for each_user in users:
        if u_id == each_user['auth_user_id']:
            num_channels_joined = each_user['channels_joined'][-1]['num_channels_joined']
    return num_channels_joined

# count the number of dms user joined
def get_num_dms_joined(u_id, users):
    num_dms_joined = 0
    for each_user in users:
        if u_id == each_user['auth_user_id']:
            num_dms_joined = each_user['dms_joined'][-1]['num_dms_joined']
    return num_dms_joined

# count the number of messages user sent
def get_num_messages_sent(u_id, users):
    num_messages_sent = 0
    for each_user in users:
        if u_id == each_user['auth_user_id']:
            num_messages_sent = each_user['messages_sent'][-1]['num_messages_sent']
    return num_messages_sent

# count the number of channel exist
def get_num_channels(store):
    return len(store['channels'])

# count the number of message exist
def get_num_dms(store):
    return len(store['dms'])

# count the number of channel exist
def get_num_messages(store):
    return store['messages_exist'][-1]['num_messages_exist']

# count the number num users who have joined at least one channel or dm
def get_rate(store):
    count = 0
    for each_user in store['users']:
        if each_user['channels_joined'][-1]['num_channels_joined'] != 0 or each_user['dms_joined'][-1]['num_dms_joined'] != 0:
            count += 1
    return count