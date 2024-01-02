import requests
from src import config
from tests.fixture import *
    
    
def test_message_react_unreact_v1(register, channel, dm):
    
    #send message
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data1 = message_id.json()
    
    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm[0]['dm_id'],
        'message' : 'qqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    dm_message_id_data2 = message_id.json()
    
    #react correcttly
    react_input = {
        'token': register[0]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 200
    
    react_input = {
        'token': register[0]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 200
    
    react_input = {
        'token': register[1]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 200
    
    react_input = {
        'token': register[1]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 200
    #react inputerror
    react_input = {
        'token': register[7]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 400
    react_input = {
        'token': register[7]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 400
    
    react_input = {
        'token': register[1]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : -1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 400
    
    react_input = {
        'token': register[0]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    react_id = requests.post(config.url + 'message/react/v1', json = react_input)
    assert react_id.status_code == 400

    #unreact inputerror
    unreact_input = {
        'token': register[7]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert react_id.status_code == 400
    unreact_input = {
        'token': register[7]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert react_id.status_code == 400
    
    unreact_input = {
        'token': register[0]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : -1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 400
    
    join_inf = {
        "token" : register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    unreact_input = {
        'token': register[2]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 400
    
    #unreact correctly
    unreact_input = {
        'token': register[0]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 200
    
    unreact_input = {
        'token': register[0]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 200
    
    unreact_input = {
        'token': register[1]['token'],
        'message_id' : message_id_data1['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 200
    
    unreact_input = {
        'token': register[1]['token'],
        'message_id' : dm_message_id_data2['message_id'],
        'react_id' : 1,
    }
    unreact_id = requests.post(config.url + 'message/unreact/v1', json = unreact_input)
    assert unreact_id.status_code == 200
#send 21 messages with tag
def senddm_tag_21(the_token,the_dm_id,user_0_handle, user_1_handle):
    counter = 0
    while counter < 21:
        senddm_input = {
            'token': the_token,
            'dm_id' : the_dm_id,
            'message' : f'@{user_0_handle} @{user_1_handle}heyaduafhuehfrhfoerhfioahefuafeioafghaouefhoh',
        }
        message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
        assert message_id.status_code == 200
        counter += 1
    

def test_notification(register, channel, dm):
    
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[0]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    assert result_user_profile_1.status_code == 200
    user_0_handle = data_user_profile_1['user']["handle_str"]
    user_profile_1 = {
        'token': register[1]['token'],
        'u_id': register[1]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    assert result_user_profile_1.status_code == 200
    user_1_handle = data_user_profile_1['user']["handle_str"]
    #send message
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : f'@{user_0_handle} hey',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200

    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : f'@hh hey',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200

    
    senddm_tag_21(register[0]['token'],dm[0]['dm_id'],user_0_handle, user_1_handle)
    
    notifications_input = {
        'token': register[0]['token'],
    }
    notifications = requests.get(config.url + 'notifications/get/v1', params = notifications_input)
    assert notifications.status_code == 200
    notifications = notifications.json()
    
    notifications_input = {
        'token': register[1]['token'],
    }
    notifications = requests.get(config.url + 'notifications/get/v1', params = notifications_input)
    assert notifications.status_code == 200
