import requests
from src.config import *
from tests.fixture import *


# test_users_all_v1 && correct
def test_users_all_v1_correct(register):
    users_all_token = {
        'token': register[0]['token']
    }
    result_users_all = requests.get(config.url + 'users/all/v1', params = users_all_token)
    data_users_all = result_users_all.json()
    assert result_users_all.status_code == 200
    assert isinstance(data_users_all, dict)
    assert isinstance(data_users_all['users'], list)
    assert data_users_all['users'][0]['u_id'] == 1
    assert data_users_all['users'][0]["email"] == 'tengbuyi@ad.unsw.edu.au'
    assert data_users_all['users'][0]["name_first"] == 'max'
    assert data_users_all['users'][0]["name_last"] == 'min'
    assert data_users_all['users'][0]["handle_str"] == 'maxmin'
    assert data_users_all['users'][0]["profile_img_url"] == default_image_address
    assert data_users_all['users'][1]["u_id"] == 2
    assert data_users_all['users'][1]["email"] == 'buyi@ad.unsw.edu.au'
    assert data_users_all['users'][1]["name_first"] == 'max'
    assert data_users_all['users'][1]["name_last"] == 'min'
    assert data_users_all['users'][1]["handle_str"] == 'maxmin0'
    assert data_users_all['users'][1]["profile_img_url"] == default_image_address

# test for removed user
def test_users_all_v1_removed_user(register):
    removed_user = {
        "token": register[0]['token'],
        "u_id": register[1]['auth_user_id']
    }
    requests.delete(config.url + 'admin/user/remove/v1', json = removed_user)
    user1_token = {
        'token': register[0]['token']
    }
    result_users_all_user1 = requests.get(config.url + 'users/all/v1', params = user1_token)
    data_users_all_user1 = result_users_all_user1.json()
    assert data_users_all_user1['users'][0]['u_id'] == 1
    assert data_users_all_user1['users'][0]["email"] == 'tengbuyi@ad.unsw.edu.au'
    assert data_users_all_user1['users'][0]["name_first"] == 'max'
    assert data_users_all_user1['users'][0]["name_last"] == 'min'
    assert data_users_all_user1['users'][0]["handle_str"] == 'maxmin'
    assert data_users_all_user1['users'][1]["u_id"] == 3
    assert data_users_all_user1['users'][1]["email"] == 'max@ad.unsw.edu.au'
    assert data_users_all_user1['users'][1]["name_first"] == 'max'
    assert data_users_all_user1['users'][1]["name_last"] == 'min'
    assert data_users_all_user1['users'][1]["handle_str"] == 'maxmin1'

# test for invalid input token
def test_users_all_v1_invalid_token(register):
    users_all_token = {
        'token': register[0]['token']
    }
    users_all_token['token'] += 'wrong_token_suffix'
    result_users_all_token = requests.get(config.url + 'users/all/v1', params = users_all_token)
    assert result_users_all_token.status_code == 403

# test for target user profile
def test_user_profile_v1_correct(register):
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[3]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    assert result_user_profile_1.status_code == 200
    assert isinstance(data_user_profile_1, dict)
    assert isinstance(data_user_profile_1['user'], dict)
    assert data_user_profile_1['user']['u_id'] == 4
    assert data_user_profile_1['user']["email"] == 'eleanor@ad.unsw.edu.au'
    assert data_user_profile_1['user']["name_first"] == 'max'
    assert data_user_profile_1['user']["name_last"] == 'min'
    assert data_user_profile_1['user']["handle_str"] == 'maxmin2'
    # # test for removed user
    # user_removed_1 = {
    #     'token': register[0]['token'],
    #     'u_id': register[1]['auth_user_id']
    # }
    # result_user_removed_1 = requests.delete(config.url + 'admin/user/remove/v1', json = user_removed_1)
    # data_user_removed_1 = result_user_removed_1.json()
    # params_2 = {
    #     'token': resp2_data['token'],
    #     'u_id': 11
    # }
    # resp = requests.get(config.url + 'user/profile/v1', params = params_2)
    # resp_data = resp.json()
    # assert resp.status_code == 200
    # assert isinstance(resp_data, dict)
    # assert isinstance(resp_data['user'], dict)
    # assert resp_data['user']['u_id'] == 11
    # assert resp_data['user']["email"] == 'tengbuyi2@ad.unsw.edu.au'
    # assert resp_data['user']["name_first"] == 'Removed'
    # assert resp_data['user']["name_last"] == 'user'
    # assert resp_data['user']["handle_str"] == 'removeduser'


# test for invalid u_id
def test_user_profile_v1_invalid_u_id(register):
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': 100
    }
    result_users_all_token = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    assert result_users_all_token.status_code == 400

# test for invalid input token
def test_user_profile_v1_invalid_token(register):
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[2]['auth_user_id']
    }
    user_profile_1['token'] += 'wrong_token_suffix'
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    assert result_user_profile_1.status_code == 403

# test for successed rename
def test_user_profile_setname_v1_correct(register):
    user_setname_1 = {
        'token': register[0]['token'],
        'name_first': 'heyden',
        'name_last': 'marc'
    }
    user_setname_2 = {
        'token': register[1]['token'],
        'name_first': 'lee',
        'name_last': 'eleanor'
    }
    # create a channel waiting for set name
    create_channel = {
        "name" : 'name1',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    channels_id = requests.post(config.url + 'channels/create/v2', json = create_channel)
    channels_id_data = channels_id.json()
    # create a dm waiting for set name
    create_dm = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = create_dm)
    dm_id_data = dm_id.json()
    # rename
    result_user_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json = user_setname_1)
    data_user_setname_1 = result_user_setname_1.json()
    result_user_setname_2 = requests.put(config.url + 'user/profile/setname/v1', json = user_setname_2)
    data_user_setname_1 = result_user_setname_1.json()
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[0]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    user_profile_2 = {
        'token': register[1]['token'],
        'u_id': register[1]['auth_user_id']
    }
    result_user_profile_2 = requests.get(config.url + 'user/profile/v1', params = user_profile_2)
    data_user_profile_2 = result_user_profile_2.json()
    assert data_user_profile_1['user']["name_first"] == 'heyden'
    assert data_user_profile_1['user']["name_last"] == 'marc'
    assert data_user_profile_2['user']["name_first"] == 'lee'
    assert data_user_profile_2['user']["name_last"] == 'eleanor'
    assert result_user_setname_1.status_code == 200
    assert result_user_setname_2.status_code == 200
    assert data_user_setname_1 == {}
    assert data_user_setname_1 == {}
    # test for user detail in channel
    detail_info = {
        "token" : register[0]['token'],
        "channel_id" : channels_id_data['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_info)
    assert channel_detail.status_code == 200
    channel_detail_data = channel_detail.json()
    assert channel_detail_data['owner_members'][0]['name_first'] == 'heyden'
    assert channel_detail_data['all_members'][0]['name_first'] == 'heyden'
    assert channel_detail_data['owner_members'][0]['name_last'] == 'marc'
    assert channel_detail_data['all_members'][0]['name_last'] == 'marc'
    # test for user detail in dm
    input_info1 = {
        'token': register[0]['token'],
        'dm_id': dm_id_data['dm_id']
    }
    dm_details1 = requests.get(config.url + 'dm/details/v1', params = input_info1)
    dm_details_data1 = dm_details1.json()
    assert dm_details1.status_code == 200
    assert dm_details_data1['members'][0]['name_first'] == 'heyden'
    assert dm_details_data1['members'][0]['name_last'] == 'marc'


# test for error input name
def test_user_profile_setname_v1_inputerror(register):
    user_setname_1 = {
        'token': register[0]['token'],
        'name_first': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
        'name_last': 'marc'
    }
    user_setname_2 = {
        'token': register[1]['token'],
        'name_first': '',
        'name_last': 'eleanor'
    }
    result_user_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json = user_setname_1)
    result_user_setname_2 = requests.put(config.url + 'user/profile/setname/v1', json = user_setname_2)
    assert result_user_setname_1.status_code == 400
    assert result_user_setname_2.status_code == 400

# test for invalid input token
def test_user_profile_setname_v1_invalid_token(register):
    user_setname_1 = {
        'token': register[0]['token'],
        'name_first': 'max',
        'name_last': 'eleanor'
    }
    user_setname_1['token'] += 'wrong_token_suffix'
    result_user_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json = user_setname_1)
    assert result_user_setname_1.status_code == 403

# test for successed reset email
def test_user_profile_setemail_v1_correct(register):
    user_setemail_1 = {
        'token': register[0]['token'],
        'email': '2236770115@qq.com'
    }
    user_setemail_2 = {
        'token': register[1]['token'],
        'email': '3365738197@qq.com'
    }
    # create a dm waiting for set name
    create_dm = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = create_dm)
    dm_id_data = dm_id.json()
    result_user_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json = user_setemail_1)
    data_user_setemail_1 = result_user_setemail_1.json()
    result_user_setemail_2 = requests.put(config.url + 'user/profile/setemail/v1', json = user_setemail_2)
    data_user_setemail_2 = result_user_setemail_2.json()
    # display profile
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[0]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    user_profile_2 = {
        'token': register[1]['token'],
        'u_id': register[1]['auth_user_id']
    }
    result_user_profile_2 = requests.get(config.url + 'user/profile/v1', params = user_profile_2)
    data_user_profile_2 = result_user_profile_2.json()
    assert data_user_profile_1['user']["email"] == '2236770115@qq.com'
    assert data_user_profile_2['user']["email"] == '3365738197@qq.com'
    assert result_user_profile_1.status_code == 200
    assert result_user_profile_2.status_code == 200
    assert result_user_setemail_1.status_code == 200
    assert result_user_setemail_2.status_code == 200
    assert data_user_setemail_1 == {}
    assert data_user_setemail_2 == {}
    # test for user detail in dm
    input_info1 = {
        'token': register[0]['token'],
        'dm_id': dm_id_data['dm_id']
    }
    dm_details1 = requests.get(config.url + 'dm/details/v1', params = input_info1)
    dm_details_data1 = dm_details1.json()
    assert dm_details1.status_code == 200
    assert dm_details_data1['members'][0]['email'] == '2236770115@qq.com'

# test for error input email
def test_user_profile_setemail_v1_inputerror(register):
    user_setemail_1 = {
        'token': register[0]['token'],
        'email': 'hithere&qm,ocj'
    }
    user_setemail_2 = {
        'token': register[1]['token'],
        'email': 'tengbuyi@ad.unsw.edu.au'
    }
    result_user_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json = user_setemail_1)
    result_user_setemail_2 = requests.put(config.url + 'user/profile/setemail/v1', json = user_setemail_2)
    assert result_user_setemail_1.status_code == 400
    assert result_user_setemail_2.status_code == 400

# test for invalid input token
def test_user_profile_setemail_v1_invalid_token(register):
    user_setemail_1 = {
        'token': register[0]['token'],
        'email': 'tengbuyi@ad.unsw.edu.au'
    }
    user_setemail_1['token'] += 'wrong_token_suffix'
    result_user_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json = user_setemail_1)
    assert result_user_setemail_1.status_code == 403

# test for successed reset handle
def test_user_profile_sethandle_v1_correct(register):
    user_sethandle_1 = {
        'token': register[0]['token'],
        'handle_str': 'heythereisastring'
    }
    user_sethandle_2 = {
        'token': register[1]['token'],
        'handle_str': 'anotherstring'
    }
    # create a dm waiting for set name
    create_dm = {
        "token": register[0]['token'],
        'u_ids': [register[1]['auth_user_id'], register[2]['auth_user_id']]
    }
    dm_id = requests.post(config.url + 'dm/create/v1', json = create_dm)
    dm_id_data = dm_id.json()
    result_user_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_1)
    data_user_sethandle_1 = result_user_sethandle_1.json()
    result_user_sethandle_2 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_2)
    data_user_sethandle_2 = result_user_sethandle_2.json()
    user_profile_1 = {
        'token': register[0]['token'],
        'u_id': register[0]['auth_user_id']
    }
    result_user_profile_1 = requests.get(config.url + 'user/profile/v1', params = user_profile_1)
    data_user_profile_1 = result_user_profile_1.json()
    user_profile_2 = {
        'token': register[1]['token'],
        'u_id': register[1]['auth_user_id']
    }
    result_user_profile_2 = requests.get(config.url + 'user/profile/v1', params = user_profile_2)
    data_user_profile_2 = result_user_profile_2.json()
    assert data_user_profile_1['user']["handle_str"] == 'heythereisastring'
    assert data_user_profile_2['user']["handle_str"] == 'anotherstring'
    assert result_user_profile_1.status_code == 200
    assert result_user_profile_2.status_code == 200
    assert result_user_sethandle_1.status_code == 200
    assert result_user_sethandle_2.status_code == 200
    assert data_user_sethandle_1 == {}
    assert data_user_sethandle_2 == {}
    # test for user detail in dm
    input_info1 = {
        'token': register[0]['token'],
        'dm_id': dm_id_data['dm_id']
    }
    dm_details1 = requests.get(config.url + 'dm/details/v1', params = input_info1)
    dm_details_data1 = dm_details1.json()
    assert dm_details1.status_code == 200
    assert dm_details_data1['members'][0]['handle_str'] == 'heythereisastring'


# test for error input
def test_user_profile_sethandle_v1_inputerror(register):
    user_sethandle_1 = {
        'token': register[0]['token'],
        'handle_str': 'ab'
    }
    user_sethandle_2 = {
        'token': register[1]['token'],
        'handle_str': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    }
    user_sethandle_3 = {
        'token': register[2]['token'],
        'handle_str': 'abc123()&^%$&$&'
    }
    user_sethandle_4 = {
        'token': register[3]['token'],
        'handle_str': 'maxmin'
    }
    result_user_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_1)
    result_user_sethandle_2 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_2)
    result_user_sethandle_3 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_3)
    result_user_sethandle_4 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_4)
    assert result_user_sethandle_1.status_code == 400
    assert result_user_sethandle_2.status_code == 400
    assert result_user_sethandle_3.status_code == 400
    assert result_user_sethandle_4.status_code == 400

# test for invalid input token
def test_user_profile_sethandle_v1_invalid_token(register):
    user_sethandle_1 = {
        'token': register[0]['token'],
        'handle_str': 'maxmin',
    }
    user_sethandle_1['token'] += 'wrong_token_suffix'
    result_user_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json = user_sethandle_1)
    assert result_user_sethandle_1.status_code == 403

# test for successfully upload photos
def test_user_profile_uploadphoto_v1_work(register, channel, dm, message):
    # test for invalid input img_url
    user_1_uploadphoto = {
        'token': message[3]['token'],
        'img_url': 'http://m.imeitou.com/uploads/allimg/211108/3-21110Q5235V63.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 400,
        'y_end': 400
    }
    result_uploadphoto_user_1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_1_uploadphoto)
    assert result_uploadphoto_user_1.status_code == 200
    assert result_uploadphoto_user_1.json() == {}
    # test for changed url in channels and dms
    user_1_profile = {
        'token': message[0]['token'],
        'u_id': register[1]['auth_user_id']
    }
    result_user_1_profile = requests.get(config.url + 'user/profile/v1', params = user_1_profile)
    data_user_1_profile = result_user_1_profile.json()
    assert data_user_1_profile['user']['profile_img_url'] == f"http://localhost:{port}/static/{user_1_profile['u_id']}.jpg"
    # in channels
    user_detail_channel = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = user_detail_channel)
    assert channel_detail.status_code == 200
    channel_detail_data = channel_detail.json()
    assert channel_detail_data['all_members'][1]['profile_img_url'] == f"http://localhost:{port}/static/{user_1_profile['u_id']}.jpg"
    # in dms
    user_1_dm = {
        'token': register[0]['token'],
        'dm_id': dm[0]['dm_id']
    }
    result_user_1_dm = requests.get(url + 'dm/details/v1', params = user_1_dm)
    data_user_1_dm = result_user_1_dm.json()
    assert result_user_1_dm.status_code == 200
    assert data_user_1_dm['members'][1]['profile_img_url'] == f"http://localhost:{port}/static/{user_1_profile['u_id']}.jpg"

# test for error upload photos
def test_user_profile_uploadphoto_v1_error(register):
    # test for input is not a url
    user_0_uploadphoto = {
        'token': register[0]['token'],
        'img_url': 'http://invalid.jpg',
        'x_start': 1,
        'y_start': 1,
        'x_end': 400,
        'y_end': 400
    }
    result_uploadphoto_user_0 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_0_uploadphoto)
    assert result_uploadphoto_user_0.status_code == 400
    # test for invalid input img_url
    user_1_uploadphoto = {
        'token': register[0]['token'],
        'img_url': 'http://m.imeitou.com/upl235V63.jpg',
        'x_start': 1,
        'y_start': 1,
        'x_end': 400,
        'y_end': 400
    }
    result_uploadphoto_user_1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_1_uploadphoto)
    assert result_uploadphoto_user_1.status_code == 400
    # test for invalid input x_start and y_start and their ends
    user_2_uploadphoto = {
        'token': register[1]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 10000,
        'y_start': 1,
        'x_end': 400,
        'y_end': 400
    }
    result_uploadphoto_user_2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_2_uploadphoto)
    assert result_uploadphoto_user_2.status_code == 400
    user_3_uploadphoto = {
        'token': register[2]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', # not found yet
        'x_start': 1,
        'y_start': 10000,
        'x_end': 400,
        'y_end': 400
    }
    result_uploadphoto_user_3 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_3_uploadphoto)
    assert result_uploadphoto_user_3.status_code == 400
    user_3_uploadphoto = {
        'token': register[2]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', # not found yet
        'x_start': 1,
        'y_start': 1,
        'x_end': 10000,
        'y_end': 400
    }
    result_uploadphoto_user_3 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_3_uploadphoto)
    assert result_uploadphoto_user_3.status_code == 400
    user_4_uploadphoto = {
        'token': register[3]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', # not found yet
        'x_start': 1,
        'y_start': 1,
        'x_end': 400,
        'y_end': 10000
    }
    result_uploadphoto_user_4 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_4_uploadphoto)
    assert result_uploadphoto_user_4.status_code == 400
    # test for start bigger than end
    user_5_uploadphoto = {
        'token': register[4]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', # not found yet
        'x_start': 100,
        'y_start': 1,
        'x_end': 10,
        'y_end': 400
    }
    result_uploadphoto_user_5 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_5_uploadphoto)
    assert result_uploadphoto_user_5.status_code == 400
    user_6_uploadphoto = {
        'token': register[5]['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', # not found yet
        'x_start': 1,
        'y_start': 100,
        'x_end': 400,
        'y_end': 10
    }
    result_uploadphoto_user_6 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_6_uploadphoto)
    assert result_uploadphoto_user_6.status_code == 400
    # test for image uploaded is not a JPG
    user_7_uploadphoto = {
        'token': register[6]['token'],
        'img_url': 'http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png', # not found yet
        'x_start': 1,
        'y_start': 1,
        'x_end': 10,
        'y_end': 10
    }
    result_uploadphoto_user_7 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = user_7_uploadphoto)
    assert result_uploadphoto_user_7.status_code == 400

# test for count a user's involvement_rate
def test_user_stats_v1_correct(message):
    user_1_stats = {
        'token': message[0]['token']
    }
    user_1_stats = requests.get(config.url + 'user/stats/v1', params = user_1_stats)
    data_user_1_stats = user_1_stats.json()
    assert data_user_1_stats['user_stats']['involvement_rate'] == 0.35
    assert len(data_user_1_stats['user_stats']['messages_sent']) - 1 == 3
    assert len(data_user_1_stats['user_stats']['dms_joined']) - 1 == 2
    assert len(data_user_1_stats['user_stats']['channels_joined']) - 1 == 2

# test for involvement_rate is zero when divisor is zero
def test_user_stats_v1_zero_divisor(register):
    user_1_stats = {
        'token': register[0]['token']
    }
    user_1_stats = requests.get(config.url + 'user/stats/v1', params = user_1_stats)
    data_user_1_stats = user_1_stats.json()
    assert data_user_1_stats['user_stats']['involvement_rate'] == 0

# test for count a user's involvement_rate more than 1
def test_user_stats_v1_correct_1():
    # register user1 and user2
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
    register_user_1 = requests.post(config.url + 'auth/register/v2', json = register_user1)
    register_user_1_data = register_user_1.json()
    register_user_2 = requests.post(config.url + 'auth/register/v2', json = register_user2)
    register_user_2_data = register_user_2.json()
    # create a channel1 with user1 and user2
    create_channel1 = {
        "name" : 'channel1',
        "token" : register_user_1_data['token'],
        "is_public": 1,
    }
    channel1_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channel1_id_data = channel1_id.json()
    invite_user2 = {
        "token" : register_user_1_data['token'],
        "channel_id" : channel1_id_data['channel_id'],
        "u_id" : register_user_2_data['auth_user_id'],
    }
    requests.post(config.url + 'channel/invite/v2', json = invite_user2)
    # user2 send 1 message
    send_channel_user2_1 = {
        'token': register_user_1_data['token'],
        'channel_id' : channel1_id_data['channel_id'],
        'message' : 'friends',
    }
    message_id_user2_1 = requests.post(config.url + 'message/send/v1', json = send_channel_user2_1)
    data_message_id_user2_1 = message_id_user2_1.json()
    # delete message from user2
    message_remove_user2_1 = {
        "token" : register_user_1_data['token'],
        "message_id" : data_message_id_user2_1['message_id'],
    }
    message_removed = requests.delete(config.url + 'message/remove/v1', json = message_remove_user2_1)
    assert message_removed.status_code == 200
    # user2's user_stats should be more than 1 but output 1
    user_2_stats = {
        'token': register_user_2_data['token']
    }
    user_2_stats = requests.get(config.url + 'user/stats/v1', params = user_2_stats)
    data_user_2_stats = user_2_stats.json()
    assert data_user_2_stats['user_stats']['involvement_rate'] == 1

# test for invalid token
def test_user_stats_v1_error(register):
    # test for invalid token
    user_1_stats = {
        'token': register[0]['token'] + '123'
    }
    user_1_stats = requests.get(config.url + 'user/stats/v1', params = user_1_stats)
    assert user_1_stats.status_code == 403

# test for count a user's involvement_rate
def test_users_stats_v1_correct(message):
    user_1_stats = {
        'token': message[0]['token']
    }
    user_1_stats = requests.get(config.url + 'users/stats/v1', params = user_1_stats)
    data_user_1_stats = user_1_stats.json()
    assert data_user_1_stats['workspace_stats']['utilization_rate'] == 0.8
    assert data_user_1_stats['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 5
    assert data_user_1_stats['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 5
    assert data_user_1_stats['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 10
    message_remove_input = {
        "token" : message[0]['token'],
        "message_id" : message[3]['message_id'],
    }
    requests.delete(config.url + 'message/remove/v1', json = message_remove_input)
    user_1_stats_2 = {
        'token': message[0]['token']
    }
    result_user_1_stats_2 = requests.get(config.url + 'users/stats/v1', params = user_1_stats_2)
    data_user_1_stats_2 = result_user_1_stats_2.json()
    assert data_user_1_stats_2['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 9

# test for invalid token
def test_users_stats_v1_error(register):
    # test for invalid token
    user_1_stats = {
        'token': register[0]['token'] + '123'
    }
    user_1_stats = requests.get(config.url + 'users/stats/v1', params = user_1_stats)
    assert user_1_stats.status_code == 403

def test_clear_for_json():
    requests.delete(config.url + 'clear/v1')