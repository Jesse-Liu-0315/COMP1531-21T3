import requests
from src import config
from tests.fixture import *

def test_search(register):
    # check whether the function work through channel/message
    create_channel_info = {
        "token" : register[0]['token'],
        "name" : 'name',
        "is_public": 1,
    }
    channels_id = requests.post(config.url + 'channels/create/v2', json = create_channel_info)
    channels_id_data = channels_id.json()
    send_input = {
        'token': register[0]['token'],
        'channel_id' : channels_id_data['channel_id'],
        'message' : '4666',
    }
    message_id = requests.post(config.url + 'message/send/v1', json = send_input)
    assert message_id.status_code == 200
    search_info = {
        'token' : register[0]['token'],
        'query_str' : '666'
    }
    search_result = requests.get(config.url + 'search/v1', params = search_info)
    search_result_data = search_result.json()
    assert search_result.status_code == 200
    assert search_result_data['messages'][0]['message'] == '4666'
    # check whether the function work through dm/message
    create_dm_info = {
        'token': register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = create_dm_info)
    dm_id_data = dm_id.json()
    dm_send_message = {
        'token' : register[0]['token'],
        'dm_id' : dm_id_data['dm_id'],
        'message' : '36666',
    }
    message_id = requests.post(config.url + 'message/senddm/v1', json = dm_send_message)
    assert message_id.status_code == 200
    search_info1 = {
        'token' : register[0]['token'],
        'query_str' : '6666'
    }
    search_result1 = requests.get(config.url + 'search/v1', params = search_info1)
    search_result_data1 = search_result1.json()
    assert search_result1.status_code == 200
    assert search_result_data1['messages'][0]['message'] == '36666'
    # check invaild token
    search_info2 = {
        'token' : -1,
        'query_str' : '6666',
    }
    search_result2 = requests.get(config.url + 'search/v1', params = search_info2)
    assert search_result2.status_code == 403
    # check InputError when:
    #    length of query_str is less than 1 or over 1000 characters
    search_info3 = {
        'token' : register[0]['token'],
        'query_str' : '',
    }
    search_result3 = requests.get(config.url + 'search/v1', params = search_info3)
    assert search_result3.status_code == 400
    search_info4 = {
        'token' : register[0]['token'],
        'query_str' : '6'*1001,
    }
    search_result4 = requests.get(config.url + 'search/v1', params = search_info4)
    assert search_result4.status_code == 400
    search_info5 = {
        'token' : register[3]['token'],
        'query_str' : '6',
    }
    search_result5 = requests.get(config.url + 'search/v1', params = search_info5)
    assert search_result5.status_code == 200
    search_result5_data = search_result5.json()
    assert search_result5_data == {'messages' : []}
    # in order to improve coverage to skip some for loop
    search_info6 = {
        'token' : register[2]['token'],
        'query_str' : '6',
    }
    search_result6 = requests.get(config.url + 'search/v1', params = search_info6)
    assert search_result6.status_code == 200
    search_result6_data = search_result6.json()
    assert search_result6_data['messages'][0]['message'] == '36666'
    search_info7 = {
        'token' : register[2]['token'],
        'query_str' : '7',
    }
    search_result7 = requests.get(config.url + 'search/v1', params = search_info7)
    assert search_result7.status_code == 200
