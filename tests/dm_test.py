import requests
from src import config
from tests.fixture import *


def test_dm_create(register):
    # test for correct result from dm_create
    user1 = register[0]
    user2 = register[1]
    user3 = register[2]
    received_info = {
        "token": user1['token'],
        'u_ids': [user2['auth_user_id'], user3['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = received_info)
    dm_id_data = dm_id.json()
    assert isinstance(dm_id_data, dict)
    assert isinstance(dm_id_data['dm_id'], int)
    assert dm_id.status_code == 200
    # test for invalid case
    received_info1 = {
        "token": user1['token'],
        'u_ids': [user2['auth_user_id'], user3['auth_user_id'], 10000]
    }
    inputerror_data = requests.post(config.url + 'dm/create/v1', json = received_info1)
    assert inputerror_data.status_code == 400

    received_info2 = {
        "token": 'fuhswofhohvsoighwoihfqio',
        'u_ids': [user2['auth_user_id'], user3['auth_user_id']]
    }
    accesserror_data = requests.post(config.url + 'dm/create/v1', json = received_info2)
    assert accesserror_data.status_code == 403


def test_dm_list(register, dm):
    # test for correct result from dm_list
    user1 = register[0]
    list_token = {
        "token": user1['token']
    }
    dm_list = requests.get(config.url + 'dm/list/v1', params = list_token)
    dm_list_data = dm_list.json()
    assert dm_list_data['dms'][0]['name'] == dm[0]['name']
    assert dm_list_data['dms'][1]['dm_id'] == dm[1]['dm_id']
    assert dm_list_data['dms'][1]['name'] == dm[1]['name']

   
    accesserror_data = requests.get(config.url + 'dm/list/v1', params = 'ushdnbdnbhosihga')
    assert accesserror_data.status_code == 403


def test_dm_remove(register, dm):
    user1 = register[0]
    user2 = register[1]
    user3 = register[2]
    list_token = {
        "token": user1['token']
    }
    dm_list = requests.get(config.url + 'dm/list/v1', params = list_token)
    dm_list_data = dm_list.json()
    assert dm_list_data['dms'][0]['name'] == dm[0]['name']
    assert dm_list_data['dms'][1]['dm_id'] == dm[1]['dm_id']
    assert dm_list_data['dms'][1]['name'] == dm[1]['name']
    input_info = {
        'token': user1['token'],
        'dm_id': dm[0]['dm_id']
    }
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = input_info)
    dm_list2 = requests.get(config.url + 'dm/list/v1', params = list_token)
    dm_list_data2 = dm_list2.json()
    assert dm_remove.status_code == 200
    assert dm_list_data2['dms'][0]['name'] == dm[1]['name']
    assert dm_list_data2['dms'][0]['dm_id'] == dm[1]['dm_id']

    accesserror_info = {
        'token': 'vhduhvpvjwpv',
        'dm_id': dm[0]['dm_id']
    }
    accesserror_data = requests.delete(config.url + 'dm/remove/v1', json = accesserror_info)
    assert accesserror_data.status_code == 403
    accesserror_info2 = {
        'token': user3['token'],
        'dm_id': dm[1]['dm_id']
    }
    accesserror_data2 = requests.delete(config.url + 'dm/remove/v1', json = accesserror_info2)
    assert accesserror_data2.status_code == 403
    # test for invalid id
    inputerror_info = {
        'token': user2['token'],
        'dm_id': 1000
    }
    inputerror_data = requests.delete(config.url + 'dm/remove/v1', json = inputerror_info)
    assert inputerror_data.status_code == 400


def test_dm_leave(register, dm):
    # test_dm_leave_correct and test_dm_leave_format
    user2 = register[1]
    leave_info = {
        "token" : user2['token'],
        "dm_id" : dm[0]['dm_id'],
    }
    resp_leave = requests.post(config.url + 'dm/leave/v1', json = leave_info)
    assert resp_leave.status_code == 200
    resp_leave_data = resp_leave.json()
    assert isinstance(resp_leave_data, dict)
    list_info = {
        "token" : user2['token'],
    }
    resp_list = requests.get(config.url + 'dm/list/v1', params = list_info)
    assert resp_list.status_code == 200
    resp_list_data = resp_list.json()
    assert resp_list_data['dms'][0]['name'] == dm[1]['name']
    # test_dm_leave AccessError when: dm_id is valid and the authorised user is not a member of the DM
    leave_info2 = {
        "token" : user2['token'],
        "dm_id" : -1,
    }
    resp_leave2 = requests.post(config.url + 'dm/leave/v1', json = leave_info2)
    assert resp_leave2.status_code == 400
    leave_info3 = {
        "token" : user2['token'],
        "dm_id" : dm[0]['dm_id'],
    }
    resp_leave3 = requests.post(config.url + 'dm/leave/v1', json = leave_info3)
    assert resp_leave3.status_code == 403
    leave_info4 = {
        "token" : -1,
        "dm_id" : dm[1]['dm_id'],
    }
    resp_leave4 = requests.post(config.url + 'dm/leave/v1', json = leave_info4)
    assert resp_leave4.status_code == 403


def test_dm_details(register, dm):
    # test for correct details
    user1 = register[0]
    user3 = register[2]
    # test for first dm
    input_info1 = {
        'token': user1['token'],
        'dm_id': dm[0]['dm_id']
    }
    dm_details1 = requests.get(config.url + 'dm/details/v1', params = input_info1)
    dm_details_data1 = dm_details1.json()
    assert dm_details1.status_code == 200
    assert dm_details_data1['name'] == dm[0]['name']
    assert dm_details_data1['members'][0]['u_id'] == dm[0]['members'][0]['u_id']
    assert dm_details_data1['members'][1]['u_id'] == dm[0]['members'][1]['u_id']
    # test for second dm
    input_info2 = {
        'token': user3['token'],
        'dm_id': dm[1]['dm_id']
    }
    dm_details2 = requests.get(config.url + 'dm/details/v1', params = input_info2)
    dm_details_data2 = dm_details2.json()
    assert dm_details2.status_code == 200
    assert dm_details_data2['name'] == dm[1]['name']
    assert dm_details_data2['members'][0]['u_id'] == dm[1]['members'][0]['u_id']

    # test for invalid token
    accesserror_info = {
        'token': 'waibibabu',
        'dm_id': dm[0]['dm_id']
    }
    accesserror_data = requests.get(config.url + 'dm/details/v1', params = accesserror_info)
    assert accesserror_data.status_code == 403
    # test for not a member of the DM
    accesserror_info2 = {
        'token': user1['token'],
        'dm_id': dm[2]['dm_id']
    }
    accesserror_data2 = requests.get(config.url + 'dm/details/v1', params = accesserror_info2)
    assert accesserror_data2.status_code == 403
    # test for invalid dm_id
    inputerror_info = {
        'token': user1['token'],
        'dm_id': 1000
    }
    inputerror_data = requests.get(config.url + 'dm/details/v1', params = inputerror_info)
    assert inputerror_data.status_code == 400
