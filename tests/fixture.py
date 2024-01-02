import pytest
import requests
from src import config

'''
def test_clear():
    register_user_ = requests.delete(config.url + 'clear/v1')
    assert json.loads(register_user_.text) == {}
    assert register_user_.status_code == 200
'''
# helper function
# register three sample user
@pytest.fixture
def register():
    requests.delete(config.url + 'clear/v1')
    register_user1 = {
        "email": 'tengbuyi@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user2 = {
        "email": 'buyi@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user3 = {
        "email": 'max@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user4 = {
        "email": 'eleanor@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user5 = {
        "email": 'mike@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user6 = {
        "email": 'jesse@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user7 = {
        "email": 'zhao@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user8 = {
        "email": 'island@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user9 = {
        "email": 'xiebro@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    register_user10 = {
        "email": 'unsw@ad.unsw.edu.au',
        "password": 'this_is_a_password',
        "name_first": 'max',
        "name_last": 'min',
    }
    users = []
    register_user_1 = requests.post(config.url + 'auth/register/v2', json = register_user1)
    register_user_1_data = register_user_1.json()
    register_user_2 = requests.post(config.url + 'auth/register/v2', json = register_user2)
    register_user_2_data = register_user_2.json()
    register_user_3 = requests.post(config.url + 'auth/register/v2', json = register_user3)
    register_user_3_data = register_user_3.json()
    register_user_4 = requests.post(config.url + 'auth/register/v2', json = register_user4)
    register_user_4_data = register_user_4.json()
    register_user_5 = requests.post(config.url + 'auth/register/v2', json = register_user5)
    register_user_5_data = register_user_5.json()
    register_user_6 = requests.post(config.url + 'auth/register/v2', json = register_user6)
    register_user_6_data = register_user_6.json()
    register_user_7 = requests.post(config.url + 'auth/register/v2', json = register_user7)
    register_user_7_data = register_user_7.json()
    register_user_8 = requests.post(config.url + 'auth/register/v2', json = register_user8)
    register_user_8_data = register_user_8.json()
    register_user_9 = requests.post(config.url + 'auth/register/v2', json = register_user9)
    register_user_9_data = register_user_9.json()
    register_user_10 = requests.post(config.url + 'auth/register/v2', json = register_user10)
    register_user_10_data = register_user_10.json()
    users.append(register_user_1_data)
    users.append(register_user_2_data)
    users.append(register_user_3_data)
    users.append(register_user_4_data)
    users.append(register_user_5_data)
    users.append(register_user_6_data)
    users.append(register_user_7_data)
    users.append(register_user_8_data)
    users.append(register_user_9_data)
    users.append(register_user_10_data)
    return users
    # sample output
    # user = [
    #     {
    #         'token': token1,
    #         'auth_user_id': 1
    #     },
    #     {
    #         'token': token2,
    #         'auth_user_id': 2
    #     },
    #     {
    #         'token': token3,
    #         'auth_user_id': 3
    #     },
    #     {
    #         'token': token4,
    #         'auth_user_id': 4
    #     },
    #     {
    #         'token': token5,
    #         'auth_user_id': 5
    #     },
    #     {
    #         'token': token6,
    #         'auth_user_id': 6
    #     },
    #     {
    #         'token': token7,
    #         'auth_user_id': 7
    #     },
    #     {
    #         'token': token8,
    #         'auth_user_id': 8
    #     },
    #     {
    #         'token': token9,
    #         'auth_user_id': 9
    #     },
    #     {
    #         'token': token10,
    #         'auth_user_id': 10
    #     }
    # ]


@pytest.fixture()
def channel(register):
    # create channels
    create_channel1 = {
        "name" : 'channel1',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    create_channel2 = {
        "name" : 'channel2',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    create_channel3 = {
        "name" : 'channel3',
        "token" : register[1]['token'],
        "is_public": 1,
    }
    create_channel4 = {
        "name" : 'channel4',
        "token" : register[2]['token'],
        "is_public": 1,
    }
    create_channel5 = {
        "name" : 'channel5',
        "token" : register[3]['token'],
        "is_public": 0,
    }
    channel1_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel2_id = requests.post(config.url + 'channels/create/v2', json = create_channel2)
    channel3_id = requests.post(config.url + 'channels/create/v2', json = create_channel3)
    channel4_id = requests.post(config.url + 'channels/create/v2', json = create_channel4)
    channel5_id = requests.post(config.url + 'channels/create/v2', json = create_channel5)
    channel1_id_data = channel1_id.json()
    channel2_id_data = channel2_id.json()
    channel3_id_data = channel3_id.json()
    channel4_id_data = channel4_id.json()
    channel5_id_data = channel5_id.json()
    # add members
    # channel1 has owner user1 and members user2
    invite_user2 = {
        "token" : register[0]['token'],
        "channel_id" : channel1_id_data['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user2)
    # channel2 has owner user1 and members user2 user3
    invite_user2 = {
        "token" : register[0]['token'],
        "channel_id" : channel2_id_data['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user2)
    invite_user3 = {
        "token" : register[0]['token'],
        "channel_id" : channel2_id_data['channel_id'],
        "u_id" : register[2]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user3)
    # channel3 has owner user2 and members user3 user5
    join_user3 = {
        "token" : register[2]['token'],
        "channel_id" : channel3_id_data['channel_id']
    }
    requests.post(config.url + 'channel/join/v2', json = join_user3)
    join_user5 = {
        "token" : register[4]['token'],
        "channel_id" : channel3_id_data['channel_id'],
    }
    requests.post(config.url + 'channel/join/v2', json = join_user5)
    # channel 4 has owner user3 and members user5 user6 user9
    invite_user5 = {
        "token" : register[2]['token'],
        "channel_id" : channel4_id_data['channel_id'],
        "u_id" : register[4]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user5)
    join_user6 = {
        "token" : register[5]['token'],
        "channel_id" : channel4_id_data['channel_id'],
    }
    requests.post(config.url + 'channel/join/v2', json = join_user6)
    invite_user9 = {
        "token" : register[2]['token'],
        "channel_id" : channel4_id_data['channel_id'],
        "u_id" : register[8]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user9)
    # channel 5 is private, owner user4 and only invite user10
    invite_user4 = {
        "token" : register[3]['token'],
        "channel_id" : channel5_id_data['channel_id'],
        "u_id" : register[9]['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user4)
    # show details
    detail_channel1 = {
        "token" : register[0]['token'],
        "channel_id" : channel1_id_data['channel_id'],
    }
    channel1_detail = requests.get(config.url + 'channel/details/v2', params = detail_channel1)
    channel1_detail_data = channel1_detail.json()
    channel1_detail_data['channel_id'] = channel1_id_data['channel_id']
    detail_channel2 = {
        "token" : register[0]['token'],
        "channel_id" : channel2_id_data['channel_id'],
    }
    channel2_detail = requests.get(config.url + 'channel/details/v2', params = detail_channel2)
    channel2_detail_data = channel2_detail.json()
    channel2_detail_data['channel_id'] = channel2_id_data['channel_id']
    detail_channel3 = {
        "token" : register[1]['token'],
        "channel_id" : channel3_id_data['channel_id'],
    }
    channel3_detail = requests.get(config.url + 'channel/details/v2', params = detail_channel3)
    channel3_detail_data = channel3_detail.json()
    channel3_detail_data['channel_id'] = channel3_id_data['channel_id']
    detail_channel4 = {
        "token" : register[2]['token'],
        "channel_id" : channel4_id_data['channel_id'],
    }
    channel4_detail = requests.get(config.url + 'channel/details/v2', params = detail_channel4)
    channel4_detail_data = channel4_detail.json()
    channel4_detail_data['channel_id'] = channel4_id_data['channel_id']
    detail_channel5 = {
        "token" : register[3]['token'],
        "channel_id" : channel5_id_data['channel_id'],
    }
    channel5_detail = requests.get(config.url + 'channel/details/v2', params = detail_channel5)
    channel5_detail_data = channel5_detail.json()
    channel5_detail_data['channel_id'] = channel5_id_data['channel_id']
    channels_detail = [channel1_detail_data, channel2_detail_data, channel3_detail_data, channel4_detail_data, channel5_detail_data]
    return channels_detail

@pytest.fixture()
def dm(register):
    # create dm
    dm_create_1 = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id']]
    }
    dm_create_2 = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_create_3 = {
        "token": register[1]['token'],
        'u_ids': [register[2]['auth_user_id'], register[4]['auth_user_id']]
    }
    dm_create_4 = {
        "token": register[2]['token'],
        'u_ids': [register[4]['auth_user_id'], register[5]['auth_user_id'], register[8]['auth_user_id']]
    }
    dm_create_5 = {
        "token": register[3]['token'],
        'u_ids': [register[9]['auth_user_id']]
    }
    result_dm_id_1 = requests.post(config.url + 'dm/create/v1', json = dm_create_1)
    result_dm_id_2 = requests.post(config.url + 'dm/create/v1', json = dm_create_2)
    result_dm_id_3 = requests.post(config.url + 'dm/create/v1', json = dm_create_3)
    result_dm_id_4 = requests.post(config.url + 'dm/create/v1', json = dm_create_4)
    result_dm_id_5 = requests.post(config.url + 'dm/create/v1', json = dm_create_5)
    dm_id_1 = result_dm_id_1.json()
    dm_id_2 = result_dm_id_2.json()
    dm_id_3 = result_dm_id_3.json()
    dm_id_4 = result_dm_id_4.json()
    dm_id_5 = result_dm_id_5.json()
    # return details
    dm_details_1 = {
        'token': register[0]['token'],
        'dm_id': dm_id_1['dm_id']
    }
    dm_details_2 = {
        'token': register[0]['token'],
        'dm_id': dm_id_2['dm_id']
    }
    dm_details_3 = {
        'token': register[1]['token'],
        'dm_id': dm_id_3['dm_id']
    }
    dm_details_4 = {
        'token': register[2]['token'],
        'dm_id': dm_id_4['dm_id']
    }
    dm_details_5 = {
        'token': register[3]['token'],
        'dm_id': dm_id_5['dm_id']
    }
    result_dm_details_1 = requests.get(config.url + 'dm/details/v1', params = dm_details_1)
    result_dm_details_2 = requests.get(config.url + 'dm/details/v1', params = dm_details_2)
    result_dm_details_3 = requests.get(config.url + 'dm/details/v1', params = dm_details_3)
    result_dm_details_4 = requests.get(config.url + 'dm/details/v1', params = dm_details_4)
    result_dm_details_5 = requests.get(config.url + 'dm/details/v1', params = dm_details_5)
    data_dm_details_1 = result_dm_details_1.json()
    data_dm_details_1['dm_id'] = dm_id_1['dm_id']
    data_dm_details_2 = result_dm_details_2.json()
    data_dm_details_2['dm_id'] = dm_id_2['dm_id']
    data_dm_details_3 = result_dm_details_3.json()
    data_dm_details_3['dm_id'] = dm_id_3['dm_id']
    data_dm_details_4 = result_dm_details_4.json()
    data_dm_details_4['dm_id'] = dm_id_4['dm_id']
    data_dm_details_5 = result_dm_details_5.json()
    data_dm_details_5['dm_id'] = dm_id_5['dm_id']
    list_dm_details = [data_dm_details_1, data_dm_details_2, data_dm_details_3, data_dm_details_4, data_dm_details_5]
    return list_dm_details

@pytest.fixture()
def message(register, channel, dm):
    # user1 send 3 message in channel1
    send_channel_user1_1 = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : 'hi',
    }
    send_channel_user1_2 = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : 'my',
    }
    send_channel_user1_3 = {
        'token': register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : 'friends',
    }
    message_id_user1_1 = requests.post(config.url + 'message/send/v1', json = send_channel_user1_1)
    result_message_id_user1_1 = message_id_user1_1.json()
    data_message_id_user1_1 = {}
    data_message_id_user1_1['message_id'] = result_message_id_user1_1['message_id']
    data_message_id_user1_1['token'] = register[0]['token']
    message_id_user1_2 = requests.post(config.url + 'message/send/v1', json = send_channel_user1_2)
    result_message_id_user1_2 = message_id_user1_2.json()
    data_message_id_user1_2 = {}
    data_message_id_user1_2['message_id'] = result_message_id_user1_2['message_id']
    data_message_id_user1_2['token'] = register[0]['token']
    message_id_user1_3 = requests.post(config.url + 'message/send/v1', json = send_channel_user1_3)
    result_message_id_user1_3 = message_id_user1_3.json()
    data_message_id_user1_3 = {}
    data_message_id_user1_3['message_id'] = result_message_id_user1_3['message_id']
    data_message_id_user1_3['token'] = register[0]['token']
    # user2 send 1 message in channel1
    send_channel_user2_1 = {
        'token': register[1]['token'],
        'channel_id' : channel[0]['channel_id'],
        'message' : 'yoo',
    }
    message_id_user2_1 = requests.post(config.url + 'message/send/v1', json = send_channel_user2_1)
    result_message_id_user2_1 = message_id_user2_1.json()
    data_message_id_user2_1 = {}
    data_message_id_user2_1['message_id'] = result_message_id_user2_1['message_id']
    data_message_id_user2_1['token'] = register[1]['token']
    # user3 sendd 2 message in channel2
    send_channel_user3_1 = {
        'token': register[2]['token'],
        'channel_id' : channel[1]['channel_id'],
        'message' : '123',
    }
    send_channel_user3_2 = {
        'token': register[2]['token'],
        'channel_id' : channel[1]['channel_id'],
        'message' : '321',
    }
    message_id_user3_1 = requests.post(config.url + 'message/send/v1', json = send_channel_user3_1)
    result_message_id_user3_1 = message_id_user3_1.json()
    data_message_id_user3_1 = {}
    data_message_id_user3_1['message_id'] = result_message_id_user3_1['message_id']
    data_message_id_user3_1['token'] = register[2]['token']
    message_id_user3_2 = requests.post(config.url + 'message/send/v1', json = send_channel_user3_2)
    result_message_id_user3_2 = message_id_user3_2.json()
    data_message_id_user3_2 = {}
    data_message_id_user3_2['message_id'] = result_message_id_user3_2['message_id']
    data_message_id_user3_2['token'] = register[2]['token']
    # user6 sendd 2 message in channel4
    send_channel_user6_1 = {
        'token': register[5]['token'],
        'channel_id' : channel[3]['channel_id'],
        'message' : '11111111',
    }
    send_channel_user6_2 = {
        'token': register[5]['token'],
        'channel_id' : channel[3]['channel_id'],
        'message' : '111111',
    }
    message_id_user6_1 = requests.post(config.url + 'message/send/v1', json = send_channel_user6_1)
    result_message_id_user6_1 = message_id_user6_1.json()
    data_message_id_user6_1 = {}
    data_message_id_user6_1['message_id'] = result_message_id_user6_1['message_id']
    data_message_id_user6_1['token'] = register[5]['token']
    message_id_user6_2 = requests.post(config.url + 'message/send/v1', json = send_channel_user6_2)
    result_message_id_user6_2 = message_id_user6_2.json()
    data_message_id_user6_2 = {}
    data_message_id_user6_2['message_id'] = result_message_id_user6_2['message_id']
    data_message_id_user6_2['token'] = register[5]['token']
    # user5 send 1 message in dm3
    send_dm_user5_1 = {
        'token': register[4]['token'],
        'dm_id' : dm[2]['dm_id'],
        'message' : 'qqq',
    }
    message_id_user5_1 = requests.post(config.url + 'message/senddm/v1', json = send_dm_user5_1)
    result_message_id_user5_1 = message_id_user5_1.json()
    data_message_id_user5_1 = {}
    data_message_id_user5_1['message_id'] = result_message_id_user5_1['message_id']
    data_message_id_user5_1['token'] = register[4]['token']
    # user10 send 1 message in dm5
    send_dm_user10_1 = {
        'token': register[9]['token'],
        'dm_id' : dm[4]['dm_id'],
        'message' : 'today is \n beautiful day',
    }
    message_id_user10_1 = requests.post(config.url + 'message/senddm/v1', json = send_dm_user10_1)
    result_message_id_user10_1 = message_id_user10_1.json()
    data_message_id_user10_1 = {}
    data_message_id_user10_1['message_id'] = result_message_id_user10_1['message_id']
    data_message_id_user10_1['token'] = register[9]['token']
    return [data_message_id_user1_1, data_message_id_user1_2, data_message_id_user1_3, data_message_id_user2_1, data_message_id_user3_1, data_message_id_user3_2, data_message_id_user6_1, data_message_id_user6_2, data_message_id_user5_1, data_message_id_user10_1]

