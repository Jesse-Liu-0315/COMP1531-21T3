import requests
from src import config
from tests.fixture import *
from datetime import datetime, timezone
import time


def test_standup_start_v1(register, channel):
    start_data = {
        'token' : register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : 1
    }
    standup_start = requests.post(config.url + '/standup/start/v1', json = start_data)
    time_stamp_finished = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 1
    standup_start_data = standup_start.json()
    assert standup_start.status_code == 200
    assert standup_start_data['time_finish'] - time_stamp_finished >= -3

    start_invalid_token = {
        'token' : register[5]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : 1
    }
    standup_accesserror = requests.post(config.url + '/standup/start/v1', json = start_invalid_token)
    assert standup_accesserror.status_code == 403
    
    start_invalid_channel_id = {
        'token' : register[1]['token'],
        'channel_id' : 1000,
        'length' : 1
    }
    standup_inputerror = requests.post(config.url + '/standup/start/v1', json = start_invalid_channel_id)
    assert standup_inputerror.status_code == 400

    start_invalid_length = {
        'token' : register[1]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : -1
    }
    standup_inputerror = requests.post(config.url + '/standup/start/v1', json = start_invalid_length)
    assert standup_inputerror.status_code == 400


def test_standup_active_v1(register, channel):
    start_data = {
        'token' : register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : 1
    }
    requests.post(config.url + '/standup/start/v1', json = start_data)
    time_stamp_finished = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    active_data = {
        'token': register[0]['token'],
        'channel_id': channel[0]['channel_id']
    }
    standup_active = requests.get(config.url + '/standup/active/v1', params = active_data)
    standup_active_data = standup_active.json()
    assert standup_active.status_code == 200
    assert standup_active_data['is_active'] == True
    assert standup_active_data['time_finish'] - time_stamp_finished >= -3

    not_member_of = {
        'token': register[5]['token'],
        'channel_id': channel[0]['channel_id']
    }
    standup_active_acesserror = requests.get(config.url + '/standup/active/v1', params = not_member_of)
    standup_active_acesserror.status_code == 403

    start_invalid_channel_id = {
        'token' : register[1]['token'],
        'channel_id' : 1000,
        'length' : 1
    }
    requests.post(config.url + '/standup/start/v1', json = start_invalid_channel_id)
    active_data = {
        'token': register[0]['token'],
        'channel_id': 10000
    }
    standup_active_inputerror = requests.get(config.url + '/standup/active/v1', params = active_data)
    assert standup_active_inputerror.status_code == 400

def test_standup_send_v1(register, channel):
    # all working situation
    start_data = {
        'token' : register[0]['token'],
        'channel_id' : channel[1]['channel_id'],
        'length' : 1
    }
    requests.post(config.url + '/standup/start/v1', json = start_data)
    send_data = {
        'token': register[0]['token'],
        'channel_id': channel[1]['channel_id'],
        'message': 'hi, how are you?'
    }
    standup_send = requests.post(config.url + '/standup/send/v1', json = send_data)
    assert standup_send.status_code == 200   

    # user not a member of the channel but channel exists
    not_member_of_data = {
        'token': register[5]['token'],
        'channel_id': channel[0]['channel_id'],
        'message': 'hello'
    } 
    standup_send_accesserror = requests.post(config.url + '/standup/send/v1', json = not_member_of_data)
    assert standup_send_accesserror.status_code == 403

    # situation of not valid channel
    invalid_channel_id = {
        'token': register[0]['token'],
        'channel_id': 1000,
        'message': 'hi, how are you?'
    }
    standup_send_inputerror = requests.post(config.url + '/standup/send/v1', json = invalid_channel_id)
    assert standup_send_inputerror.status_code == 400

    # situation of too long message
    invalid_messgae_length = {
        'token': register[0]['token'],
        'channel_id': channel[0]['channel_id'],        
        'message': 'a' * 2000
    }
    standup_send_inputerror = requests.post(config.url + '/standup/send/v1', json = invalid_messgae_length)
    assert standup_send_inputerror.status_code == 400

    # all working situation
    start_data = {
        'token' : register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : 1
    }
    requests.post(config.url + '/standup/start/v1', json = start_data)
    send_data = {
        'token': register[0]['token'],
        'channel_id': channel[0]['channel_id'],
        'message': 'hi, how are you?'
    }
    standup_send = requests.post(config.url + '/standup/send/v1', json = send_data)
    assert standup_send.status_code == 200
    # get the active status
    active_data = {
        'token': register[0]['token'],
        'channel_id': channel[0]['channel_id']
    }
    time.sleep(1)
    active = requests.get(config.url + '/standup/active/v1', params = active_data)
    active_data = active.json()
    assert active.status_code == 200
    assert active_data['is_active'] == False

def test_alreadyrunning_standup(register, channel):
    start_already_active = {
        'token' : register[0]['token'],
        'channel_id' : channel[0]['channel_id'],
        'length' : 1
    }
    standup_inputerror1 = requests.post(config.url + '/standup/start/v1', json = start_already_active)
    assert standup_inputerror1.status_code == 200
    standup_inputerror2 = requests.post(config.url + '/standup/start/v1', json = start_already_active)
    assert standup_inputerror2.status_code == 400


def test_not_standup_running(register, channel):
    # situation of standup is not active
    not_active_data = {
        'token': register[0]['token'],
        'channel_id': channel[0]['channel_id'],
        'message': 'hello'
    } 
    standup_send_inputerror = requests.post(config.url + '/standup/send/v1', json = not_active_data)
    assert standup_send_inputerror.status_code == 400
