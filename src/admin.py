from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import *

def get_user(token):
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = decoded['u_id']
    return user_id

def check_user_id(u_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == u_id and user['name_first'] != 'Removed':
            return True
    return False
        

def check_only_global_owner(u_id):
    store = data_store.get()
    all_owners = []
    for user in store['users']:
        if user['permission_id'] == 1:
            all_owners.append(user['auth_user_id'])
    for owner in all_owners:
        if owner == u_id and len(all_owners) == 1:
            return False
    return True

def check_auth_global_owner(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id and user['permission_id'] == 1:
            return True
    return False

def check_permission(permission_id):
    if permission_id != 1 and permission_id != 2:
        raise InputError('permission_id is invalid')


def admin_user_remove_v1(token, u_id):
    '''
    Input a token and an u_id. If the token is an admin token, 
    remove the user by u_id. Their messages would be 
    replaced by 'Removed user', and name would be replaced by 
    'Removed' (first name), 'user' (last name).

    Arguments:
        token (string)    - get user details by token
        uid (integer)    - remove an user accoding to u_id

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user 
                    who is the only global owner
        AccessError - Occurs when the authorised user is not a global owner

    Return Value:
        Returns empty dictionary
    '''
    store = data_store.get()
    # using check functions above
    check_valid_token(token, store['token'])
    auth_user_id = get_user(token)
    check2 = check_auth_global_owner(auth_user_id)
    if check2 == False:
        raise AccessError('the authorised user is not a global owner')
    check1 = check_user_id(u_id)
    if check1 == False:
        raise InputError('u_id does not refer to a valid user')
    check3 = check_only_global_owner(u_id)
    if check3 == False:
        raise InputError('u_id refers to a user who is the only global owner')

    # remove the user in users
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['name_first'] = 'Removed'
            user['name_last'] = 'user'
            user['email'] = ''
            user['handle'] = ''
            user['removed'] = True
    # remove the user in all channels
    for channel in store['channels']:
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(owner)
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    # remove the user in all dms
    for each_dms in store['dms']:
        for member in each_dms['all_members']:
            if member['u_id'] == u_id:
                each_dms['all_members'].remove(member)
        for message in each_dms['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    
    data_store.set(store)
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Input a token, an u_id and a permission_id. If the token 
    is an admin token, change the user's permission_id by their u_id.

    Arguments:
        token (string)    - get user details by token
        uid (integer)    - remove an user accoding to u_id
        permission_id (integer)    - replace the original premission_id

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is the only 
                    global owner and they are being demoted to a user
                    - Occurs when permission_id is invalid
        AccessError - Occurs when the authorised user is not a global owner

    Return Value:
        Returns empty dictionary
    '''
    store = data_store.get()
    # using check functions above
    check_valid_token(token, store['token'])
    auth_user_id = get_user(token)
    check2 = check_auth_global_owner(auth_user_id)
    if check2 == False:
        raise AccessError('the authorised user is not a global owner')
    check1 = check_user_id(u_id)
    if check1 == False:
        raise InputError('u_id does not refer to a valid user')
    check3 = check_only_global_owner(u_id)
    if check3 == False:
        raise InputError('u_id refers to a user who is the only global owner')
    check_permission(permission_id)

    # change the original permisssion_id
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['permission_id'] = permission_id
    data_store.set(store)
    return {}
