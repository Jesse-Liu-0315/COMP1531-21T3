import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.auth import *
from src.channels import *
from src.channel import *
from src.error import *
from src.user import *
from src.dm import *
from src.message import *
from src.admin import *
from src.standup import *
from src.notifications import *
from src.search import *
from src.share import *
from src.pin_and_unpin import *
from src import config

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path = '/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS
# Login existed user with correct password
@APP.route("/auth/login/v2", methods = ['POST'])
def login():
    data = request.get_json()
    result = auth_login_v2(data['email'], data['password'])
    return dumps(result)

# Regisrer a new user
@APP.route("/auth/register/v2", methods = ['POST'])
def register():
    data = request.get_json()
    result = auth_register_v2(data['email'], data['password'], data['name_first'], data['name_last'])
    return dumps(result)

# Logout the target user
@APP.route("/auth/logout/v1", methods = ['POST'])
def logout():
    data = request.get_json()
    result = auth_logout_v1(data['token'])
    return dumps(result)

# Create a channel
@APP.route('/channels/create/v2', methods = ['POST'])
def create_new_channel():
    channel_data = request.get_json()
    result = channels_create_v1(channel_data['token'], channel_data['name'], channel_data['is_public'])
    return dumps(result)

# List all channel
@APP.route('/channels/list/v2', methods = ['GET'])
def channel_list():
    channel_list_data = request.args.get('token')
    result = channels_list_v1(channel_list_data)
    return dumps(result)

# List all channel
@APP.route('/channels/listall/v2', methods = ['GET'])
def channel_listall():
    channel_listall_data = request.args.get('token')
    result = channels_listall_v1(channel_listall_data) 
    return dumps(result)

# List details of all channel
@APP.route("/channel/details/v2", methods = ['GET'])
def details():
    data_token = request.args.get('token')
    data_id = request.args.get('channel_id')
    result = channel_details_v2(data_token, data_id)
    return dumps(result)

# Invites a user with ID u_id to join a channel with ID channel_id
@APP.route("/channel/invite/v2", methods = ['POST'])
def invite():
    invite_data = request.get_json()
    result = channel_invite_v2(invite_data['token'], invite_data['channel_id'], invite_data['u_id'])
    return dumps(result)

# Add user to that channel
@APP.route("/channel/join/v2", methods = ['POST'])
def join():
    join_data = request.get_json()
    result = channel_join_v2(join_data['token'], join_data['channel_id'])
    return dumps(result)

# Retrieve messages in channel
@APP.route("/channel/messages/v2", methods = ['GET'])
def message():
    message_data_token = request.args.get('token')
    message_data_channel = request.args.get('channel_id')
    message_data_start = request.args.get('start')
    result = channel_messages_v2(message_data_token, message_data_channel, message_data_start)
    return dumps(result)

# Remove given user from the channel
@APP.route("/channel/leave/v1", methods = ['POST'])
def channel_leave():
    leave_data = request.get_json()
    result = channel_leave_v1(leave_data['token'], leave_data['channel_id'])
    return dumps(result)

# Make user with user id u_id an owner of the channel
@APP.route("/channel/addowner/v1", methods = ['POST'])
def channel_addowner():
    addowner_data = request.get_json()
    result = channel_addowner_v1(addowner_data['token'], addowner_data['channel_id'], addowner_data['u_id'])
    return dumps(result)

# Remove user with user id u_id as an owner of the channel
@APP.route("/channel/removeowner/v1", methods = ['POST'])
def channel_removeowner():
    removeowner_data = request.get_json()
    result = channel_removeowner_v1(removeowner_data['token'], removeowner_data['channel_id'], removeowner_data['u_id'])
    return dumps(result)

# Create a dm
@APP.route('/dm/create/v1', methods = ['POST'])
def create_dm():
    dm_data = request.get_json()
    result = dm_create_v1(dm_data['token'], dm_data['u_ids'])
    return dumps(result)

# Returns the list of DMs
@APP.route('/dm/list/v1', methods = ['GET'])
def dm_list():
    dm_list_data = request.args.get('token')
    result = dm_list_v1(dm_list_data)
    return dumps(result)

# Remove an existing DM
@APP.route('/dm/remove/v1', methods = ['DELETE'])
def remove_dm():
    remove_dm_data = request.get_json()
    result = dm_remove_v1(remove_dm_data['token'], remove_dm_data['dm_id'])
    return dumps(result)

# Return target details of dm
@APP.route('/dm/details/v1', methods = ['GET'])
def details_dm():
    details_token = request.args.get('token')
    details_dm_id = request.args.get('dm_id')
    result = dm_details_v1(details_token, details_dm_id)
    return dumps(result)

# Remove user from this DM
@APP.route('/dm/leave/v1', methods = ['POST'])
def leave_dm():
    leave_dm_data = request.get_json()
    result = dm_leave_v1(leave_dm_data['token'], leave_dm_data['dm_id'])
    return dumps(result)

# Retrieve messages in dm
@APP.route("/dm/messages/v1", methods = ['GET'])
def dm_message():
    data1 = request.args.get('token')
    data2 = request.args.get('dm_id')
    data3 = request.args.get('start')
    result = dm_messages_v1(data1, data2, data3)
    return dumps(result)

# Send message to dm
@APP.route('/message/senddm/v1', methods = ['POST'])
def message_senddm():
    data = request.get_json()
    result = message_senddm_v1(data['token'], data['dm_id'], data['message'])
    return dumps(result)

# Send a message from the authorised user to the channel specified by channel_id
@APP.route('/message/send/v1', methods = ['POST'])
def message_send():
    data = request.get_json()
    result = message_send_v1(data['token'], data['channel_id'], data['message'])
    return dumps(result)

# Update given message text with new text
@APP.route('/message/edit/v1', methods = ['PUT'])
def message_edit():
    data = request.get_json()
    result = message_edit_v1(data['token'], data['message_id'], data['message'])
    return dumps(result)

# Remove message
@APP.route('/message/remove/v1', methods = ['DELETE'])
def message_remove():
    data = request.get_json()
    result = message_remove_v1(data['token'], data['message_id'])
    return dumps(result)

# List all users
@APP.route('/users/all/v1', methods = ['GET'])
def users_all():
    token = request.args.get('token')
    result = users_all_v1(token)
    return dumps(result)

# List target user's profile
@APP.route('/user/profile/v1', methods = ['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    result = user_profile_v1(token, u_id)
    return dumps(result)

# reset the user's name
@APP.route('/user/profile/setname/v1', methods = ['PUT'])
def user_rename():
    data = request.get_json()
    result = user_profile_setname_v1(data['token'], data['name_first'], data['name_last'])
    return dumps(result)

# reset the user's email
@APP.route('/user/profile/setemail/v1', methods = ['PUT'])
def user_reset_email():
    data = request.get_json()
    result = user_profile_setemail_v1(data['token'], data['email'])
    return dumps(result)

# reset the user's handle
@APP.route('/user/profile/sethandle/v1', methods = ['PUT'])
def user_reset_handle():
    data = request.get_json()
    result = user_profile_sethandle_v1(data['token'], data['handle_str'])
    return dumps(result)

# Remove an user as an admin
@APP.route("/admin/user/remove/v1", methods = ['DELETE'])
def admin_user_remove():
    remove_user = request.get_json()
    token = remove_user['token']
    u_id = remove_user['u_id']
    result = admin_user_remove_v1(token, u_id)
    return dumps(result)

# Set their permissions to new permissions described by permission_id
@APP.route("/admin/userpermission/change/v1", methods = ['POST'])
def admin_userpermission_change():
    change_user = request.get_json()
    token = change_user['token']
    u_id = change_user['u_id']
    permission_id = change_user['permission_id']
    result = admin_userpermission_change_v1(token, u_id, permission_id)
    return dumps(result)

#-------------------- iterate 3 --------------------#

@APP.route('/notifications/get/v1', methods = ['GET'])
def notifications_get():
    token = request.args.get('token')
    result = notifications_get_v1(token)
    return dumps(result)

    
@APP.route('/search/v1', methods = ['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    result = search_v1(token, query_str)
    return dumps(result)


@APP.route('/message/share/v1', methods = ['POST'])
def message_share():
    data = request.get_json()
    result = message_share_v1(data['token'], data['og_message_id'], data['message'], data['channel_id'], data['dm_id'])
    return dumps(result)


@APP.route('/message/react/v1', methods = ['POST'])
def message_react():
    data = request.get_json()
    result = message_react_v1(data['token'], data['message_id'], data['react_id'])
    return dumps(result)


@APP.route('/message/unreact/v1', methods = ['POST'])
def message_unreact():
    data = request.get_json()
    result = message_unreact_v1(data['token'], data['message_id'], data['react_id'])
    return dumps(result)


@APP.route('/message/pin/v1', methods = ['POST'])
def message_pin():
    data = request.get_json()
    result = message_pin_v1(data['token'], data['message_id'])
    return dumps(result)


@APP.route('/message/unpin/v1', methods = ['POST'])
def message_unpin():
    data = request.get_json()
    result = message_unpin_v1(data['token'], data['message_id'])
    return dumps(result)


@APP.route('/message/sendlater/v1', methods = ['POST'])
def message_sendlater():
    sendlater_data = request.get_json()
    sendlater_result = message_sendlater_v1(sendlater_data['token'], sendlater_data['channel_id'], sendlater_data['message'], sendlater_data['time_sent'])
    return dumps(sendlater_result)


@APP.route('/message/sendlaterdm/v1', methods = ['POST'])
def message_sendlaterdm():
    data = request.get_json()
    result = message_sendlaterdm_v1(data['token'], data['dm_id'], data['message'], data['time_sent'])
    return dumps(result)


@APP.route('/standup/start/v1', methods = ['POST'])
def standup_start():
    data = request.get_json()
    result = standup_start_v1(data['token'], data['channel_id'], data['length'])
    return dumps(result)


@APP.route('/standup/active/v1', methods = ['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    result = standup_active_v1(token, channel_id)
    return dumps(result)


@APP.route('/standup/send/v1', methods = ['POST'])
def standup_send():
    data = request.get_json()
    result = standup_send_v1(data['token'], data['channel_id'], data['message'])
    return dumps(result)


@APP.route('/auth/passwordreset/request/v1', methods = ['POST'])
def auth_passwordreset_request():
    data = request.get_json()
    result = auth_passwordreset_request_v1(data['email'])
    return dumps(result)


@APP.route('/auth/passwordreset/reset/v1', methods = ['POST'])
def auth_passwordreset_reset():
    data = request.get_json()
    result = auth_passwordreset_reset_v1(data['reset_code'], data['new_password'])
    return dumps(result)


@APP.route('/user/profile/uploadphoto/v1', methods = ['POST'])
def user_profile_uploadphoto():
    data = request.get_json()
    result = user_profile_uploadphoto_v1(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end'])
    return dumps(result)


@APP.route('/static/<file_name>', methods = ['GET'])
def send_photo_to_json(file_name):
    return send_from_directory('../static', file_name)


@APP.route('/user/stats/v1', methods = ['GET'])
def user_stats():
    token = request.args.get('token')
    result = user_stats_v1(token)
    return dumps(result)


@APP.route('/users/stats/v1', methods = ['GET'])
def users_stats():
    token = request.args.get('token')
    result = users_stats_v1(token)
    return dumps(result)


# Clear stored data
@APP.route("/clear/v1", methods = ['DELETE'])
def clear():
    return dumps(clear_v1())

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
