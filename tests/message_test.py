import requests
from src import config
from tests.fixture import *
from threading import Timer
from datetime import datetime, timezone

def test_message_send(register):

    create_channel1 = {
        "name" : 'name',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    channel_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel_id_data = channel_id.json()
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    # message_id_data = message_id.json()
    # message_id_data = message_id_data
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    # message_id_data = message_id.json()
    send_input = {
        'token': register[0]['token'],
        'channel_id' : -999,
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 400
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 403
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : '',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 400
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'a'*1001,
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 400

def test_message_edit(register):
    #create
    create_channel1 = {
        "name" : 'name',
        "token" : register[1]['token'],
        "is_public": 1,
    }
    channel_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel_id_data = channel_id.json()
    
    received_info = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data = dm_id.json()
    #send
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    # message_id_data = message_id.json()
    # message_id_data = message_id_data
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data2 = message_id.json()
    senddm_input = {
        'token': register[1]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'qqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data3 = message_id.json()
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qqqq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data4 = message_id.json()
    #edit1
    message_edit_input = {
        "token" : register[1]['token'],
        "message_id" : message_id_data2['message_id'],
        'message' : 'mahuateng'
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 200
    message_info = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['end'] == -1
    assert channel_message_data['messages'][1]['message'] == 'mahuateng'
    assert len(channel_message_data['messages']) == 3
    #edit2
    message_edit_input = {
        "token" : register[1]['token'],
        "message_id" : message_id_data2['message_id'],
        'message' : ''
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 200

    message_info = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['end'] == -1
    assert len(channel_message_data['messages']) == 2
    #edit3
    message_edit_input = {
        "token" : register[1]['token'],
        "message_id" : -999,
        'message' : 'a'
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 400
    
    message_info = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    message_info = {
        "token" : register[2]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    assert len(channel_message_data['messages']) == 2
    assert len(dm_message_data['messages']) == 1
    #edit4
    message_edit_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data3['message_id'],
        'message' : 'z'
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    input_info1 = {
        'token': register[0]['token'],
        'dm_id': dm_id_data['dm_id']
    }
    dm_details1 = requests.get(config.url + 'dm/details/v1', params = input_info1)
    assert dm_details1.status_code == 200
    assert message_edit.status_code == 403
    #edit5
    join_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    message_edit_input = {
        "token" : register[0]['token'],
        "message_id" : message_id_data4['message_id'],
        'message' : 'z'
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 200
    message_info = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['messages'][0]['message'] == 'z'
    #edit6
    join_inf = {
        "token" : register[2]['token'],
        "channel_id" : channel_id_data['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    send_input = {
        'token': register[2]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qqqqq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data5 = message_id.json()
    message_edit_input = {
        "token" : register[1]['token'],
        "message_id" : message_id_data5['message_id'],
        'message' : 'sss'
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 200
    message_info = {
        "token" : register[2]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['messages'][2]['message'] == 'q'
    #edit7
    message_edit_input = {
        "token" : register[1]['token'],
        "message_id" : message_id_data3['message_id'],
        'message' : 'a'*1001,
    }
    message_edit = requests.put(config.url + 'message/edit/v1', json = message_edit_input)
    assert message_edit.status_code == 400

def test_message_remove(register):
    #create
    create_channel1 = {
        "name" : 'name',
        "token" : register[2]['token'],
        "is_public": 1,
    }
    channel_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel_id_data2 = channel_id.json()
    join_inf = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data2['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    
    create_channel1 = {
        "name" : 'name',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    channel_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel_id_data = channel_id.json()

    join_inf = {
        "token" : register[1]['token'],
        "channel_id" : channel_id_data['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    
    
    received_info = {
        "token": register[2]['token'],
        'u_ids': [register[1]['auth_user_id'], register[0]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data2 = dm_id.json()

    received_info = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data = dm_id.json()
    
    #send
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data = message_id.json()

    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data2 = message_id.json()

    senddm_input = {
        'token': register[1]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'qqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data3 = message_id.json()

    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'qqqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data4 = message_id.json()

    #newsend
    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data2['channel_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data5 = message_id.json()

    send_input = {
        'token': register[1]['token'],
        'channel_id' : channel_id_data2['channel_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data6 = message_id.json()

    senddm_input = {
        'token': register[1]['token'],
        'dm_id' : dm_id_data2['dm_id'],
        'message' : 'qqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data7 = message_id.json()

    senddm_input = {
        'token': register[1]['token'],
        'dm_id' : dm_id_data2['dm_id'],
        'message' : 'qqqq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data8 = message_id.json()
    
    #remove1
    message_remove_input = {
        "token" : register[0]['token'],
        "message_id" : -999,
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 400
    #remove2
    message_remove_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data4['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 403
    #removeall
    message_remove_input = {
        "token" : register[0]['token'],
        "message_id" : message_id_data4['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200
    
    message_info = {
        "token" : register[2]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    assert dm_message_data['messages'][0]['message'] == 'qqq'
    
    message_remove_input = {
        "token" : register[0]['token'],
        "message_id" : message_id_data3['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200

    message_remove_input = {
        "token" : register[0]['token'],
        "message_id" : message_id_data2['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200

    message_remove_input = {
        "token" : register[1]['token'],
        "message_id" : message_id_data['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200
    #removenew
    message_remove_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data5['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200
    
    message_remove_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data6['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 200
    
    message_remove_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data7['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    
    input_info1 = {
        'token': register[2]['token'],
        'dm_id': dm_id_data2['dm_id']
    }
    requests.get(config.url + 'dm/details/v1', params = input_info1)
    message_info = {
        "token" : register[2]['token'],
        "dm_id" : dm_id_data2['dm_id'],
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    print(dm_message_data)

    assert message_remove.status_code == 403
    
    message_remove_input = {
        "token" : register[2]['token'],
        "message_id" : message_id_data8['message_id'],
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    assert message_remove.status_code == 403

def test_message_senddm(register):

    #create
    received_info = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data = dm_id.json()

    #senddm
    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : -999,
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 400
 
    senddm_input = {
        'token': register[2]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 403

    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 400

    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data3 = message_id.json()
    message_id_data3 = message_id_data3

    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'a'*1001,
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 400
    
def senddm_66message(the_register_0, dm_id_data):
    
    counter = 0

    while counter < 66:
        senddm_input = {
            'token': the_register_0['token'],
            'dm_id' : dm_id_data['dm_id'],
            'message' : '666',
        }
        message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
        assert message_id.status_code == 200
        counter = counter + 1
    message_id_data = message_id.json()
    return message_id_data


def test_dm_message(register):
    
    received_info = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data = dm_id.json()

    
    message_info = {
        "token" : register[0]['token'],
        "dm_id" : -999,
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 400

    message_info = {
        "token" : register[0]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : -1,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 400

    message_info = {
        "token" : register[2]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 403


    
    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'q',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data = message_id.json()
    message_id_data = message_id_data

    message_info = {
        "token" : register[1]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    print(dm_message_data)
    assert dm_message_data['end'] == -1

    message_id_data = senddm_66message(register[0], dm_id_data)
    message_info = {
        "token" : register[1]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 6,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    print(dm_message_data)
    assert dm_message_data['end'] == 56
    
    senddm_input = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'qq',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = senddm_input)
    assert message_id.status_code == 200
    message_id_data = message_id.json()
    
    message_info = {
        "token" : register[1]['token'],
        "dm_id" : dm_id_data['dm_id'],
        "start" : 56,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    print(dm_message_data)
    assert dm_message_data['end'] == -1


def send_66message(the_register_0, channel_id_data):
    
    counter = 0

    while counter < 66:
        send_input = {
            'token': the_register_0['token'],
            'channel_id' : channel_id_data['channel_id'],
            'message' : '666',
        }
        message_id = requests.post(config.url + 'message/send/v1', json = send_input)
        assert message_id.status_code == 200
        counter = counter + 1
    message_id_data = message_id.json()
    return message_id_data

def test_channel_message_coverage(register):

    create_channel1 = {
        "name" : 'name',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    channel_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel_id_data = channel_id.json()

    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : '666',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_info = {
        "token" : register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    print(channel_message_data)

    message_id_data = send_66message(register[0], channel_id_data)
    message_id_data = message_id_data
    message_info = {
        "token" : register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 6,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['end'] == 56
    print(channel_message_data)
    
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channel_id_data['channel_id'],
        'message' : '666',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    message_id_data = message_id.json()
    
    message_info = {
        "token" : register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "start" : 56,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    print(channel_message_data)
    assert channel_message_data['end'] == -1


def test_message_send_later(register):
    # test message/sendlater/v1 work and return correct
    create_channel_info = {
        "token" : register[0]['token'],
        "name" : 'name',
        "is_public": 1,
    }
    channels_id = requests.post(config.url + 'channels/create/v2', json = create_channel_info)
    channels_id_data = channels_id.json()
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    late_time = 1
    message_send_later = {
        'token': register[0]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id = requests.post(config.url + 'message/sendlater/v1', json = message_send_later)
    assert message_id.status_code == 200
    message_id_data = message_id.json()
    assert message_id_data['message_id'] == 1
    # use remove function to check whether the message exist
    timer = Timer(late_time, check_send_message_late_remove, [register[0]['token'], message_id_data['message_id'], channels_id_data['channel_id']])
    timer.start()
    # test for InputError when any of:
    #    channel_id does not refer to a valid channel
    #    length of message is over 1000 characters
    #    time_sent is a time in the past
    # AccessError when:
    #    channel_id is valid and the authorised user is not a member of the channel they are trying to post to
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    message_send_later1 = {
        'token': register[0]['token'],
        'channel_id' : -1,
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id1 = requests.post(config.url + 'message/sendlater/v1', json = message_send_later1)
    assert message_id1.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    message_send_later2 = {
        'token': register[0]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : '',
        'time_sent' : present_time + late_time,
    }
    message_id2 = requests.post(config.url + 'message/sendlater/v1', json = message_send_later2)
    assert message_id2.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    message_send_later3 = {
        'token': register[0]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : 'a'*1001,
        'time_sent' : present_time + late_time,
    }
    message_id3 = requests.post(config.url + 'message/sendlater/v1', json = message_send_later3)
    assert message_id3.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    message_send_later4 = {
        'token': register[0]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : '666',
        'time_sent' : present_time - late_time,
    }
    message_id4 = requests.post(config.url + 'message/sendlater/v1', json = message_send_later4)
    assert message_id4.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    message_send_later5 = {
        'token': register[1]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id5 = requests.post(config.url + 'message/sendlater/v1', json = message_send_later5)
    assert message_id5.status_code == 403

# the function for timer use
def check_send_message_late_remove(token, message_id, channel_id):
    channel_message_info = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = channel_message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['messages'][0]['message'] == '666'
    message_remove_info = {
        'token' : token,
        'message_id' : message_id
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_info)
    assert message_remove.status_code == 200

def test_message_sendlaterdm(register):
    # test message/sendlater/v1 work and return correct 
    create_dm_info = {
        'token': register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = create_dm_info)
    dm_id_data = dm_id.json()
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    late_time = 1
    dm_send_later = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later)
    message_id_data = message_id.json()
    # use remove function to check whether the message exist
    timer = Timer(late_time, check_send_dmmessage_late_remove, [register[0]['token'], message_id_data['message_id'], dm_id_data['dm_id']])
    timer.start()
    # test for InputError when any of:
    #    dm_id does not refer to a valid DM
    #    length of message is over 1000 characters
    #    time_sent is a time in the past
    # AccessError when:
    #    dm_id is valid and the authorised user is not a member of the DM they are trying to post to
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    dm_send_later1 = {
        'token': register[0]['token'],
        'dm_id' : -1,
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id1 = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later1)
    assert message_id1.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    dm_send_later2 = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '',
        'time_sent' : present_time + late_time,
    }
    message_id2 = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later2)
    assert message_id2.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    dm_send_later3 = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : 'a'*1001,
        'time_sent' : present_time + late_time,
    }
    message_id3 = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later3)
    assert message_id3.status_code == 400
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    dm_send_later4 = {
        'token': register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '666',
        'time_sent' : present_time - late_time,
    }
    message_id4 = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later4)
    assert message_id4.status_code == 400
    # check access error
    present_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    dm_send_later5 = {
        'token': register[3]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '666',
        'time_sent' : present_time + late_time,
    }
    message_id5 = requests.post(config.url + 'message/sendlaterdm/v1', json = dm_send_later5)
    assert message_id5.status_code == 403

# the function for timer use
def check_send_dmmessage_late_remove(token, message_id, dm_id):
    dm_message_info = {
        "token" : token,
        "dm_id" : dm_id,
        "start" : 0,
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = dm_message_info)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    assert dm_message_data['messages'][0]['message'] == '666'
    message_remove_info = {
        'token' : token,
        'message_id' : message_id
    }
    message_remove = requests.delete(config.url + 'message/remove/v1', json = message_remove_info)
    assert message_remove.status_code == 200
