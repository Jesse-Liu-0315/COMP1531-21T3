import requests
from src import config
from tests.fixture import *


# For channels_create_v2,check the returned value, status_code
def test_channels_create(register):
    # test_channels_create_v1_format & correct
    user1 = register[0]['token']
    create_info = {
        "name": 'channel',
        "token": user1,
        "is_public": 1,
    }
    result_create1 = requests.post(config.url + 'channels/create/v2', json = create_info)
    result_create1_data = result_create1.json()
    assert isinstance(result_create1_data, dict)
    assert isinstance(result_create1_data['channel_id'], int)
    assert result_create1.status_code == 200

    # test_channels_create_v1_inputerror
    create_info1 = {
        "token": user1,
        "name": '',
        "is_public": 1,
    }
    result_create2 = requests.post(config.url + 'channels/create/v2', json = create_info1)
    assert result_create2.status_code == 400
    create_info2 = {
        "token": 'fsijosigoigjiwpgjeb',
        "name": 'abcdefghijklmnopqrstuvwxyz',
        "is_public": 0,
    }
    result_create3 = requests.post(config.url + 'channels/create/v2', json = create_info2)
    assert result_create3.status_code == 403
    

# For channels_list_v2,check the returned value, status_code
def test_channels_list(register, channel):
    # test_channels_list_v1_format & correct
    user1 = register[0]['token']
    user2 = register[1]['token']
    list_info = {
        "token": user1,
    }
    list_in = requests.get(config.url + 'channels/list/v2', params = list_info)
    list_in_data = list_in.json()
    assert list_in.status_code == 200
    assert isinstance(list_in_data, dict)
    assert isinstance(list_in_data['channels'], list)
    assert isinstance(list_in_data['channels'][0]['channel_id'], int)
    assert isinstance(list_in_data['channels'][0]['name'], str)
    assert list_in_data['channels'][0]['name'] == channel[0]['name']
    assert list_in_data['channels'][0]['channel_id'] == channel[0]['channel_id']

    list_info2 = {
        "token": 'fsijosigoigjiwpgjeb',
    }
    list_in_accesserror = requests.get(config.url + 'channels/list/v2', json = list_info2)
    assert list_in_accesserror.status_code == 403

    list_info3 = {
        "token": user2,
    }
    list_in2 = requests.get(config.url + 'channels/list/v2', params = list_info3)
    list_in2_data = list_in2.json()
    assert list_in2.status_code == 200
    assert list_in2_data['channels'][0]['name'] == channel[0]['name']
    assert list_in2_data['channels'][0]['channel_id'] == channel[0]['channel_id']

# For channels_list_v2,check the returned value, status_code of an empty list
def test_empty_channels_list(register):
    user1 = register[0]['token']
    # test_channels_list_v1_result_many
    list_info2 = {
        "token": user1,
    }
    not_in_list = requests.get(config.url + 'channels/list/v2', params = list_info2)
    not_in_list_data = not_in_list.json()
    assert len(not_in_list_data['channels']) == 0


# For channels_listall_v2,check the returned value, status_code
def test_channels_listall_v1_route(register, channel):
    user1 = register[0]['token']
    listall_info = {
        "token": user1,
    }
    listall_result_user_onse = requests.get(config.url + 'channels/listall/v2', params = listall_info) 
    listall_result_user_onse_data = listall_result_user_onse.json()

    assert listall_result_user_onse.status_code == 200

    assert isinstance(listall_result_user_onse_data, dict)
    assert isinstance(listall_result_user_onse_data['channels'], list)
    assert listall_result_user_onse_data['channels'][0]['name'] == channel[0]['name']
    assert listall_result_user_onse_data['channels'][0]['channel_id'] == channel[0]['channel_id']
    assert listall_result_user_onse_data['channels'][1]['name'] == channel[1]['name']
    assert listall_result_user_onse_data['channels'][1]['channel_id'] == channel[1]['channel_id']

    list_accesserror = {
        "token": 'fsijosiehrjewpgjeb',
    }
    list_accesserror = requests.get(config.url + 'channels/listall/v2', json = list_accesserror)
    assert list_accesserror.status_code == 403
