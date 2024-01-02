from src import config
from tests.fixture import *
import requests


def test_admin_remove(register, channel, dm, message):
    # same user send message first in dm
    send_dm_user_1 = {
        'token': register[1]['token'],
        'dm_id' : dm[0]['dm_id'],
        'message' : 'qqq',
    }
    requests.post(config.url + 'message/senddm/v1', json = send_dm_user_1)
    remove_user_1 = {
        "token": register[0]['token'],
        "u_id": register[1]['auth_user_id'],
    }
    result_remove_user_1 = requests.delete(config.url + 'admin/user/remove/v1', json = remove_user_1)
    assert result_remove_user_1.status_code == 200
    # test for message removed in channel
    message_user_channel_1 = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "start" : 0
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_user_channel_1)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert channel_message_data['messages'][0]['message'] == 'Removed user'
    # test for message removed in dm
    message_user_dm_1 = {
        'token' : register[0]['token'],
        "dm_id" : dm[0]['dm_id'],
        "start" : 0
    }
    dm_message = requests.get(config.url + 'dm/messages/v1', params = message_user_dm_1)
    assert dm_message.status_code == 200
    dm_message_data = dm_message.json()
    assert dm_message_data['messages'][0]['message'] == 'Removed user'


def test_admin_remove_invalid_token(register):
    received_info = {
        "token": register[0]['token'] + '123',
        "u_id": register[0]['auth_user_id'],
    }
    resp4 = requests.delete(config.url + 'admin/user/remove/v1', json = received_info)
    assert resp4.status_code == 403


def test_admin_remove_invalid_uid(register):
    received_info = {
        "token": register[0]['token'],
        "u_id": 11,
    }
    resp2 = requests.delete(config.url + 'admin/user/remove/v1', json = received_info)
    assert resp2.status_code == 400


def test_admin_remove_only_global_owner(register):
    received_info = {
        "token": register[0]['token'],
        "u_id": register[0]['auth_user_id'],
    }
    resp2 = requests.delete(config.url + 'admin/user/remove/v1', json = received_info)
    assert resp2.status_code == 400


def test_admin_remove_not_by_global_owner(register):
    received_info = {
        'token' : register[1]['token'],
        'u_id' : register[2]['token']
    }
    resp4 = requests.delete(config.url + 'admin/user/remove/v1', json = received_info)
    assert resp4.status_code == 403


def test_admin_change(register):
    received_info = {
        'token' : register[0]['token'],
        'u_id' : register[1]['auth_user_id'],
        'permission_id' : 1,
    }
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1', json = received_info)
    assert resp4.status_code == 200


def test_admin_change_invalid_uid(register):
    received_info = {
        'token' : register[0]['token'],
        'u_id' : 11,
        'permission_id' : 1,
    }
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1', json = received_info)
    assert resp4.status_code == 400


def test_admin_change_only_global_owner(register):
    received_info = {
        'token' : register[0]['token'],
        'u_id' : register[0]['auth_user_id'],
        'permission_id' : 2,
    }
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1', json = received_info)
    assert resp4.status_code == 400


def test_admin_change_with_invalid_permission(register):
    # change the second user's permission
    received_info = {
        'token' : register[0]['token'],
        'u_id' : register[1]['auth_user_id'],
        'permission_id' : 3,
    }
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1', json = received_info)
    assert resp4.status_code == 400


def test_admin_change_not_by_global_owner(register):
    received_info = {
        'token' : register[5]['token'],
        'u_id' : register[0]['auth_user_id'],
        'permission_id' : 1,
    }
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1', json = received_info)
    assert resp4.status_code == 403

