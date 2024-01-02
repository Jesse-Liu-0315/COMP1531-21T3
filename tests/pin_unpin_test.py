import requests
from src import config
from tests.fixture import *

def test_correct_pin_and_unpin(message, register):
    # test pin function
    message_pin1 = {
        'token': message[0]['token'],
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin1)
    assert result.status_code == 200
    # test unpin function
    message_pin2 = {
        'token': register[3]['token'],
        'message_id': 10
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin2)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin2)
    assert result.status_code == 200

def test_invalid_token(message):
    # if input token is invalid
    # Access Error (403)
    message_pin1 = {
        'token': message[0]['token'] + '123',
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 403

def test_invalid_id(message):
    # if input message_id is invalid
    # Input Error (400)
    # channel message
    message_pin = {
        'token': message[0]['token'],
        'message_id': 500
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin)
    assert result.status_code == 400
    # dm message
    message_unpin = {
        'token': message[0]['token'],
        'message_id': 500
    }
    result = requests.post(config.url + 'message/unpin/v1', json = message_unpin)
    assert result.status_code == 400

def test_alread_pinned(message, register):
    # if selected message is alread pinned
    # Input Error (400)
    # channel message
    message_pin1 = {
        'token': message[0]['token'],
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 400
    # dm message
    message_pin2 = {
        'token': register[3]['token'],
        'message_id': 10
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin2)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/pin/v1', json = message_pin2)
    assert result.status_code == 400

def test_alread_unpinned(message, register):
    # if selected message is alread unpinned
    # Input Error (400)
    # channel message
    message_pin1 = {
        'token': message[0]['token'],
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin1)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin1)
    assert result.status_code == 400
    # dm message
    message_pin2 = {
        'token': register[3]['token'],
        'message_id': 10
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin2)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin2)
    assert result.status_code == 200
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin2)
    assert result.status_code == 400

def test_no_permission(message, register):
    # if authorised user is not owner
    # Access Error (403)
    # channel message pin
    message_pin1 = {
        'token': message[8]['token'],
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin1)
    assert result.status_code == 403
    # channel message unpin
    message_pin2 = {
        'token': message[0]['token'],
        'message_id': 1
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin2)
    assert result.status_code == 200
    
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin1)
    assert result.status_code == 403
    # dm message pin
    message_pin3 = {
        'token': register[2]['token'],
        'message_id': 10
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin3)
    assert result.status_code == 403
    # dm message unpin
    message_pin4 = {
        'token': register[1]['token'],
        'message_id': 9
    }
    result = requests.post(config.url + 'message/pin/v1', json = message_pin4)
    assert result.status_code == 200

    message_pin5 = {
        'token': register[2]['token'],
        'message_id': 9
    }
    result = requests.post(config.url + 'message/unpin/v1', json = message_pin5)
    assert result.status_code == 403

