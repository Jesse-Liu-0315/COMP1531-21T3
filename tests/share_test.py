import requests
from src import config
from tests.fixture import *

def test_message_share_v1_correct(register, message):
    # share message from channel to channel
    message_share_1 = {
        'token': message[0]['token'],
        'og_message_id': 2,
        'message': 'share this message to channel2',
        'channel_id': 2,
        'dm_id': -1
    }
    result_message_share_1 = requests.post(config.url + 'message/share/v1', json = message_share_1)
    assert result_message_share_1.status_code == 200
    # share message from channel to dm
    message_share_2 = {
        'token': message[0]['token'],
        'og_message_id': 2,
        'message': 'share this message to dm2',
        'channel_id': -1,
        'dm_id': 2
    }
    result_message_share_2 = requests.post(config.url + 'message/share/v1', json = message_share_2)
    assert result_message_share_2.status_code == 200
    # share message from dm to dm
    message_share_3 = {
        'token': register[4]['token'],
        'og_message_id': 9,
        'message': 'share this message to dm4',
        'channel_id': -1,
        'dm_id': 4
    }
    result_message_share_3 = requests.post(config.url + 'message/share/v1', json = message_share_3)
    assert result_message_share_3.status_code == 200
    # share message from dm to channel
    message_share_4 = {
        'token': register[9]['token'],
        'og_message_id': 10,
        'message': 'share this message to channel5',
        'channel_id': 5,
        'dm_id': -1
    }
    result_message_share_4 = requests.post(config.url + 'message/share/v1', json = message_share_4)
    assert result_message_share_4.status_code == 200
    # share shared message
    message_share_5 = {
        'token': register[9]['token'],
        'og_message_id': 10,
        'message': 'share this message to channel5',
        'channel_id': 5,
        'dm_id': -1
    }
    result_message_share_5 = requests.post(config.url + 'message/share/v1', json = message_share_5)
    assert result_message_share_5.status_code == 200


def test_message_share_v1_error(register, message):
    # test for both invalid channel and dm id
    message_share_1 = {
        'token': message[0]['token'],
        'og_message_id': 2,
        'message': '',
        'channel_id': 999,
        'dm_id': 999
    }
    result_message_share_1 = requests.post(config.url + 'message/share/v1', json = message_share_1)
    assert result_message_share_1.status_code == 400
    # tser for both are not -1
    message_share_2 = {
        'token': message[0]['token'],
        'og_message_id': 2,
        'message': '',
        'channel_id': 2,
        'dm_id': 2
    }
    result_message_share_2 = requests.post(config.url + 'message/share/v1', json = message_share_2)
    assert result_message_share_2.status_code == 400
    # test for og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    message_share_3 = {
        'token': message[0]['token'],
        'og_message_id': 9,
        'message': '',
        'channel_id': -1,
        'dm_id': 1
    }
    result_message_share_3 = requests.post(config.url + 'message/share/v1', json = message_share_3)
    assert result_message_share_3.status_code == 400
    # test for 1000 characters
    message_share_4 = {
        'token': register[1]['token'],
        'og_message_id': 5,
        'message': 'friends'*1000,
        'channel_id': 3,
        'dm_id': -1
    }
    result_message_share_4 = requests.post(config.url + 'message/share/v1', json = message_share_4)
    assert result_message_share_4.status_code == 400
    # test for user not in dm/channel
    message_share_5 = {
        'token': register[9]['token'],
        'og_message_id': 5,
        'message': '',
        'channel_id': 2,
        'dm_id': -1
    }
    result_message_share_5 = requests.post(config.url + 'message/share/v1', json = message_share_5)
    assert result_message_share_5.status_code == 403
    # test for invalid token
    message_share_6 = {
        'token': '123',
        'og_message_id': 5,
        'message': '',
        'channel_id': 2,
        'dm_id': -1
    }
    result_message_share_6 = requests.post(config.url + 'message/share/v1', json = message_share_6)
    assert result_message_share_6.status_code == 403

