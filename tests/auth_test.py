import requests
from src import config
from tests.fixture import *


# test for successfully register
def test_auth_register_v2_correct():
    # test for correct result and format
    requests.delete(config.url + 'clear/v1')
    register_user1 = {
        "email" : 'xiebro@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'mynamemorethan',
        "name_last" : 'tenwords',
    }
    result_register_user1 = requests.post(config.url + 'auth/register/v2', json = register_user1)
    data_register_user1 = result_register_user1.json()
    assert result_register_user1.status_code == 200
    assert isinstance(data_register_user1['token'], str)
    assert data_register_user1['auth_user_id'] == 1
    # call profile to compare handle_str
    profile_user1 = {
        'token': data_register_user1['token'],
        'u_id': data_register_user1['auth_user_id'],
    }
    result_profile_user1 = requests.get(config.url + 'user/profile/v1', params = profile_user1)
    data_profile_user_1 = result_profile_user1.json()
    assert data_profile_user_1['user']['u_id'] == 1
    assert data_profile_user_1['user']["handle_str"] == 'mynamemorethantenwor'
    # test for changing handle_str same name
    register_user2 = {
        "email" : 'hibro@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'abc',
        "name_last" : 'def',
    }
    result_register_user2 = requests.post(config.url + 'auth/register/v2', json = register_user2)
    data_register_user2 = result_register_user2.json()
    assert data_register_user2['auth_user_id'] == 2
    register_user3 = {
        "email" : 'heybro@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'abc',
        "name_last" : 'def0',
    }
    result_register_user3 = requests.post(config.url + 'auth/register/v2', json = register_user3)
    data_register_user3 = result_register_user3.json()
    assert data_register_user3['auth_user_id'] == 3
    register_user4 = {
        "email" : 'heybro1@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'abc',
        "name_last" : 'def',
    }
    result_register_user4 = requests.post(config.url + 'auth/register/v2', json = register_user4)
    data_register_user4 = result_register_user4.json()
    assert data_register_user4['auth_user_id'] == 4
    # call profile to test handle_str
    profile_user2 = {
        'token': data_register_user4['token'],
        'u_id': data_register_user4['auth_user_id'],
    }
    result_profile_user2 = requests.get(config.url + 'user/profile/v1', params = profile_user2)
    data_profile_user_2 = result_profile_user2.json()
    assert data_profile_user_2['user']['u_id'] == 4
    assert data_profile_user_2['user']["handle_str"] == 'abcdef1'

# test for invalid email in register
def test_auth_register_v2_error():
    # register one valid user
    requests.delete(config.url + 'clear/v1')
    register_user0 = {
        "email" : 'xiebro@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'max',
        "name_last" : 'min',
    }
    requests.post(config.url + 'auth/register/v2', json = register_user0)
    # test for invalid email
    register_user1 = {
        "email" : 'buyi_teng&^%$((*^&',
        "password" : 'this_is_a_password',
        "name_first" : 'max',
        "name_last" : 'min',
    }
    result_register_user1 = requests.post(config.url + 'auth/register/v2', json = register_user1)
    assert result_register_user1.status_code == 400
    # test for used email
    register_user2 = {
        "email" : 'xiebro@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'max',
        "name_last" : 'min',
    }
    result_register_user2 = requests.post(config.url + 'auth/register/v2', json = register_user2)
    assert result_register_user2.status_code == 400
    # test for invalid first and last name
    register_user3 = {
        "email" : 'z5320333@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
        "name_last" : 'min',
    }
    register_user4 = {
        "email" : 'z5320711@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : '',
        "name_last" : 'min',
    }
    register_user5 = {
        "email" : 'z53207@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'max',
        "name_last" : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
    }
    register_user6 = {
        "email" : 'z5320@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
        "name_first" : 'max',
        "name_last" : '',
    }
    result_register_user3 = requests.post(config.url + 'auth/register/v2', json = register_user3)
    result_register_user4 = requests.post(config.url + 'auth/register/v2', json = register_user4)
    result_register_user5 = requests.post(config.url + 'auth/register/v2', json = register_user5)
    result_register_user6 = requests.post(config.url + 'auth/register/v2', json = register_user6)
    assert result_register_user3.status_code == 400
    assert result_register_user4.status_code == 400
    assert result_register_user5.status_code == 400
    assert result_register_user6.status_code == 400
    # test for invalid password
    register_user7 = {
        "email" : 'newemail@ad.unsw.edu.au',
        "password" : '123',
        "name_first" : 'max',
        "name_last" : 'min',
    }
    result_register_user7 = requests.post(config.url + 'auth/register/v2', json = register_user7)
    assert result_register_user7.status_code == 400


def test_auth_login_v2_correct(register):
    # test for correct result
    login_user1 = {
        "email" : 'tengbuyi@ad.unsw.edu.au',
        "password" : 'this_is_a_password',
    }
    result_login_user1 = requests.post(config.url + 'auth/login/v2', json = login_user1)
    data_login_user1 = result_login_user1.json()
    assert isinstance(data_login_user1['token'], str)
    assert data_login_user1['auth_user_id'] == 1
    assert register[0]['token'] != data_login_user1['token']
    assert register[0]['auth_user_id'] == data_login_user1['auth_user_id']
    assert result_login_user1.status_code == 200

def test_auth_login_v2_error(register):
    assert len(register) == 10
    # test for unenroll email
    login_user1 = {
        "email" : 'z532333@ad.unsw.edu.au',
        "password" : '123456',
    }
    result_login_user1 = requests.post(config.url + 'auth/login/v2', json = login_user1)
    assert result_login_user1.status_code == 400
    # test for wrong password
    login_user2 = {
        "email" : 'tengbuyi@ad.unsw.edu.au',
        "password" : 'this_is_a_wrong_password',
    }
    result_login_user2 = requests.post(config.url + 'auth/login/v2', json = login_user2)
    assert result_login_user2.status_code == 400


# test for successfully logout
def test_auth_logout_v1_correct(register):
    logout_user1 = {
        "token" : register[0]['token'],
    }
    result_logout_user1 = requests.post(config.url + 'auth/logout/v1', json = logout_user1)
    data_logout_user1 = result_logout_user1.json()
    assert data_logout_user1 == {}
    assert result_logout_user1.status_code == 200

# test for invalid input token
def test_auth_logout_v1_error(register):
    logout_user1 = {
        'token': register[0]['token'],
        'handle_str': 'maxmin',
    }
    logout_user1['token'] += 'wrong_token_suffix'
    result_logout_user1 = requests.post(config.url + 'auth/logout/v1', json = logout_user1)
    assert result_logout_user1.status_code == 403

# test for reset password request
def test_auth_passwordreset_request_v1_correct():
    register_user1 = {
        "email" : '971795865@qq.com',
        "password" : 'this_is_a_password',
        "name_first" : 'Mik',
        "name_last" : 'e',
    }
    requests.post(config.url + 'auth/register/v2', json = register_user1)
    passwordreset_request_user1 = {
        'email': register_user1['email']
    }
    result_passwordreset_request_user1 = requests.post(config.url + 'auth/passwordreset/request/v1', json = passwordreset_request_user1)
    assert result_passwordreset_request_user1.status_code == 200

# test for reset password error
def test_auth_passwordreset_request_v1_error(register):
    assert len(register) == 10
    # test unregister email, but should be succeed
    requests.delete(config.url + 'clear/v1')
    passwordreset_request_user1 = {
        'email': 'xiebro@qq.com'
    }
    result_passwordreset_request_user1 = requests.post(config.url + 'auth/passwordreset/request/v1', json = passwordreset_request_user1)
    assert result_passwordreset_request_user1.status_code == 200
    # test invalid email, but should be succeed
    passwordreset_request_user1 = {
        'email': '89qir&*))()_+901{]>'
    }
    result_passwordreset_request_user1 = requests.post(config.url + 'auth/passwordreset/request/v1', json = passwordreset_request_user1)
    assert result_passwordreset_request_user1.status_code == 200

# Because the random numbers generated by this equation cannot be accessed by any equation,
# function 'auth/passwordreset/reset/v1' cannot be tested as success.

# test for reset password reset function error
def test_auth_passwordreset_reset_v1_error(register):
    assert len(register) == 10
    # test for password entered is less than 6 characters long
    passwordreset_reset_user1 = {
        'reset_code': 'whatever',
        'new_password': '987'
    }
    result_passwordreset_reset_user1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json = passwordreset_reset_user1)
    assert result_passwordreset_reset_user1.status_code == 400
    # test for invalid reset code
    passwordreset_request_user2 = {
        'email': 'max@ad.unsw.edu.au'
    }
    requests.post(config.url + 'auth/passwordreset/request/v1', json = passwordreset_request_user2)
    passwordreset_reset_user1 = {
        'reset_code': '(*^*&$&$)&))',
        'new_password': '987654'
    }
    result_passwordreset_reset_user1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json = passwordreset_reset_user1)
    assert result_passwordreset_reset_user1.status_code == 400