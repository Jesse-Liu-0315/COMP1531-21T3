import requests
from src import config
from tests.fixture import *


def test_detail(register, channel):
    # test for correct result about channel1 created in fixture
    detail_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    assert channel_detail.status_code == 200
    channel_detail_data = channel_detail.json()
    assert channel_detail_data['name'] == 'channel1'
    assert channel_detail_data['is_public'] == 1
    assert channel_detail_data['all_members'][0]['u_id'] == register[0]['auth_user_id']
    # test for InputError when:channel_id does not refer to a valid channel
    # AccessError when: channel_id is valid and the authorised user is not a member of the channel
    detail_inf2 = {
        "token" : register[0]['token'],
        "channel_id" : -1,
    }
    channel_detail2 = requests.get(config.url + 'channel/details/v2', params = detail_inf2)
    assert channel_detail2.status_code == 400
    detail_inf3 = {
        "token" : register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    channel_detail3 = requests.get(config.url + 'channel/details/v2', params = detail_inf3)
    assert channel_detail3.status_code == 403
    detail_inf4 = {
        "token" : '-1',
        "channel_id" : channel[0]['channel_id'],
    }
    channel_detail4 = requests.get(config.url + 'channel/details/v2', params = detail_inf4)
    assert channel_detail4.status_code == 403

def test_invite(register):
    # test for correct result in channel 1
    create_channel1 = {
        "name" : 'name',
        "token" : register[0]['token'],
        "is_public": 1,
    }
    channels_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channels_id_data = channels_id.json()
    invite_inf = {
        "token" : register[0]['token'],
        "channel_id" : channels_id_data['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    invite_return = requests.post(config.url + 'channel/invite/v2', json = invite_inf)
    assert invite_return.status_code == 200
    detail_inf = {
        "token" : register[1]['token'],
        "channel_id" : channels_id_data['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    assert channel_detail.status_code == 200
    channel_detail_data = channel_detail.json()
    assert channel_detail_data['name'] == create_channel1['name']
    assert channel_detail_data['is_public'] == 1
    assert channel_detail_data['all_members'][0]['u_id'] == register[0]['auth_user_id']
    assert channel_detail_data['all_members'][1]['u_id'] == register[1]['auth_user_id']
    # test for InputError when any of:
    #    channel_id does not refer to a valid channel
    #    u_id does not refer to a valid user
    #    u_id refers to a user who is already a member of the channel
    # AccessError when:
    #    channel_id is valid and the authorised user is not a member of the channel
    invite_inf2 = {
        "token" : register[0]['token'],
        "channel_id" : -1,
        "u_id" : register[2]['auth_user_id'],
    }
    invite_return2 = requests.post(config.url + 'channel/invite/v2', json = invite_inf2)
    assert invite_return2.status_code == 400
    invite_inf3 = {
        "token" : register[0]['token'],
        "channel_id" : channels_id_data['channel_id'],
        "u_id" : -1,
    }
    invite_return3 = requests.post(config.url + 'channel/invite/v2', json = invite_inf3)
    assert invite_return3.status_code == 400
    invite_inf4 = {
        "token" : register[0]['token'],
        "channel_id" : channels_id_data['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    invite_return4 = requests.post(config.url + 'channel/invite/v2', json = invite_inf4)
    assert invite_return4.status_code == 400
    invite_inf5 = {
        "token" : register[2]['token'],
        "channel_id" : channels_id_data['channel_id'],
        "u_id" : register[2]['auth_user_id'],
    }
    invite_return5 = requests.post(config.url + 'channel/invite/v2', json = invite_inf5)
    assert invite_return5.status_code == 403
    invite_inf6 = {
        "token" : '-1',
        "channel_id" : channels_id_data['channel_id'],
        "u_id" : register[2]['auth_user_id'],
    }
    invite_return6 = requests.post(config.url + 'channel/invite/v2', json = invite_inf6)
    assert invite_return6.status_code == 403

def test_join(register):
    # test for correct result joined in channel 1
    create_channel1 = {
        "token" : register[0]['token'],
        "name" : 'name',
        "is_public": 1,
    }
    channels_id = requests.post(config.url + 'channels/create/v2', json = create_channel1)
    channels_id_data = channels_id.json()
    join_inf = {
        "token" : register[1]['token'],
        "channel_id" : channels_id_data['channel_id'],
    }
    join_return = requests.post(config.url + 'channel/join/v2', json = join_inf)
    assert join_return.status_code == 200
    detail_inf = {
        "token" : register[1]['token'],
        "channel_id" : channels_id_data['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    channel_detail_data = channel_detail.json()
    assert channel_detail_data['name'] == 'name'
    assert channel_detail_data['is_public'] == 1
    assert channel_detail_data['all_members'][0]['u_id'] == register[0]['auth_user_id']
    assert channel_detail_data['all_members'][1]['u_id'] == register[1]['auth_user_id']
    # test for InputError when any of:
    #    channel_id does not refer to a valid channel
    #    the authorised user is already a member of the channel
    # AccessError when:
    #    channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner
    join_inf2 = {
        "token" : register[2]['token'],
        "channel_id" : -1,
    }
    join_return2 = requests.post(config.url + 'channel/join/v2', json = join_inf2)
    assert join_return2.status_code == 400
    join_inf3 = {
        "token" : register[0]['token'],
        "channel_id" : channels_id_data['channel_id'],
    }
    join_return3 = requests.post(config.url + 'channel/join/v2', json = join_inf3)
    assert join_return3.status_code == 400

    create_channel2 = {
        "token" : register[2]['token'],
        "name" : 'channel2',
        "is_public": 0,
    }
    channels_id2 = requests.post(config.url + 'channels/create/v2', json = create_channel2)
    channels_id_data2 = channels_id2.json()
    join_inf4 = {
        "token" : register[1]['token'],
        "channel_id" : channels_id_data2['channel_id'],
    }
    join_return4 = requests.post(config.url + 'channel/join/v2', json = join_inf4)
    assert join_return4.status_code == 403
    join_inf5 = {
        "token" : '-1',
        "channel_id" : channels_id_data2['channel_id'],
    }
    join_return5 = requests.post(config.url + 'channel/join/v2', json = join_inf5)
    assert join_return5.status_code == 403

def test_message(register, channel):
    # test for correct return format
    message_info = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "start" : 0,
    }
    channel_message = requests.get(config.url + 'channel/messages/v2', params = message_info)
    assert channel_message.status_code == 200
    channel_message_data = channel_message.json()
    assert isinstance(channel_message_data, dict)
    assert isinstance(channel_message_data['messages'], list)
    assert isinstance(channel_message_data['start'], int)
    assert isinstance(channel_message_data['end'], int)
    # test for InputError when any of:
    #    channel_id does not refer to a valid channel
    #    start is greater than the total number of messages in the channel
    # AccessError when:
    #    channel_id is valid and the authorised user is not a member of the channel
    message_info2 = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "start" : -1,
    }
    channel_message2 = requests.get(config.url + 'channel/messages/v2', params = message_info2)
    assert channel_message2.status_code == 400
    message_info3 = {
        "token" : register[0]['token'],
        "channel_id" : -1,
        "start" : 0,
    }
    channel_message3 = requests.get(config.url + 'channel/messages/v2', params = message_info3)
    assert channel_message3.status_code == 400
    message_info4 = {
        "token" : register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
        "start" : 0,
    }
    channel_message4 = requests.get(config.url + 'channel/messages/v2', params = message_info4)
    assert channel_message4.status_code == 403
    message_info5 = {
        "token" : '-1',
        "channel_id" : channel[0]['channel_id'],
        "start" : 0,
    }
    channel_message5 = requests.get(config.url + 'channel/messages/v2', params = message_info5)
    assert channel_message5.status_code == 403

def test_channel_leave(register, channel):
    # test_channel_leave_correct and test_channel_leave_format in channel 2 created in fixture
    # wrong token
    leave_inf0 = {
        "token" : '-1',
        "channel_id" : channel[1]['channel_id'],
    }
    leave_resp0 = requests.post(config.url + 'channel/leave/v1', json = leave_inf0)
    assert leave_resp0.status_code == 403
    leave_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
    }
    leave_resp3 = requests.post(config.url + 'channel/leave/v1', json = leave_inf)
    assert leave_resp3.status_code == 200
    leave_resp3_data = leave_resp3.json()
    assert isinstance(leave_resp3_data, dict)
    detail_inf = {
        "token": register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    channel_detail_data = channel_detail.json()
    assert len(channel_detail_data['all_members']) == 2
    assert len(channel_detail_data['owner_members']) == 0
    # InputError when: channel_id does not refer to a valid channel
    leave_inf2 = {
        "token" : register[0]['token'],
        "channel_id" : -1,
    }
    leave_resp4 = requests.post(config.url + 'channel/leave/v1', json = leave_inf2)
    assert leave_resp4.status_code == 400
    # AccessError when: channel_id is valid and the authorised user is not a member of the channel
    leave_inf3 = {
        "token" : register[3]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    leave_resp5 = requests.post(config.url + 'channel/leave/v1', json = leave_inf3)
    assert leave_resp5.status_code == 403
    leave_inf4 = {
        "token" : register[1]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    leave_resp6 = requests.post(config.url + 'channel/leave/v1', json = leave_inf4)
    assert leave_resp6.status_code == 200
    detail_inf = {
        "token": register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    channel_detail2 = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    channel_detail_data2 = channel_detail2.json()
    assert len(channel_detail_data2['owner_members']) == 1
    assert len(channel_detail_data2['all_members']) == 1
    
def test_channel_addowner(register, channel):
    # test_channel_addowner_correct and test_channel_addowner_format
    # test for correct result in channel1 
    received_info = {
        "name": 'channel',
        "token": register[1]['token'],
        "is_public": 1,
    }
    channel_id_resp1 = requests.post(config.url + 'channels/create/v2', json = received_info)
    channel_id_data = channel_id_resp1.json()
    join_inf = {
        "token": register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
    }
    requests.post(config.url + 'channel/join/v2', json = join_inf)
    addowner_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    addowner_resp3 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf)
    assert addowner_resp3.status_code == 200
    addowner_resp3_data = addowner_resp3.json()
    assert isinstance(addowner_resp3_data, dict)
    detail_inf = {
        "token": register[0]['token'],
        "channel_id" : channel_id_data['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    channel_detail_data = channel_detail.json()
    assert len(channel_detail_data['owner_members']) == 2
    assert channel_detail_data['owner_members'][1]['u_id'] == register[0]['auth_user_id']
    addowner_inf0 = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    requests.post(config.url + 'channel/addowner/v1', json = addowner_inf0)
    # test_channel_addowner InputError in channel 2 created in fixture when any of:
    # channel_id does not refer to a valid channel
    # u_id does not refer to a valid user
    # u_id refers to a user who is not a member of the channel
    # u_id refers to a user who is already an owner of the channel
    addowner_inf2 = {
        "token" : register[0]['token'],
        "channel_id" : -1,
        "u_id" : register[2]['auth_user_id'],
    }
    addowner_resp5 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf2)
    assert addowner_resp5.status_code == 400
    addowner_inf3 = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : -1,
    }
    addowner_resp6 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf3)
    assert addowner_resp6.status_code == 400
    addowner_inf4 = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[3]['auth_user_id'],
    }
    addowner_resp7 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf4)
    assert addowner_resp7.status_code == 400
    addowner_inf5 = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    addowner_resp8 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf5)
    assert addowner_resp8.status_code == 400
    join_inf3 = {
        "token": register[3]['token'],
        "channel_id" : channel[1]['channel_id'],
    }
    requests.post(config.url + 'channel/join/v2', json = join_inf3)
    # channel_id is valid and the authorised user does not have owner permissions in the channel
    addowner_inf6 = {
        "token" : register[2]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[3]['auth_user_id'],
    }
    addowner_resp9 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf6)
    assert addowner_resp9.status_code == 403
    addowner_inf7 = {
        "token" : '-1',
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[3]['auth_user_id'],
    }
    addowner_resp10 = requests.post(config.url + 'channel/addowner/v1', json = addowner_inf7)
    assert addowner_resp10.status_code == 403

def test_channel_removeowner(register, channel):
    # test for correct input and result in channel 2 created in fixture 
    addowner_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    requests.post(config.url + 'channel/addowner/v1', json = addowner_inf)
    removeowner_inf = {
        "token" : register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    removeowner_resp3 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf)
    assert removeowner_resp3.status_code == 200
    detail_inf = {
        "token": register[0]['token'],
        "channel_id" : channel[1]['channel_id'],
    }
    channel_detail = requests.get(config.url + 'channel/details/v2', params = detail_inf)
    channel_detail_data = channel_detail.json()
    assert len(channel_detail_data['owner_members']) == 1
    assert channel_detail_data['owner_members'][0]['u_id'] == register[1]['auth_user_id']
    # test for InputError when any of:
    #    channel_id does not refer to a valid channel
    #    u_id does not refer to a valid user
    #    u_id refers to a user who is not an owner of the channel
    #    u_id refers to a user who is currently the only owner of the channel
    addowner_inf2 = {
        "token" : register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    requests.post(config.url + 'channel/addowner/v1', json = addowner_inf2)
    removeowner_inf2 = {
        "token" : register[1]['token'],
        "channel_id" : -1,
        "u_id" : register[0]['auth_user_id'],
    }
    removeowner_resp4 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf2)
    assert removeowner_resp4.status_code == 400
    removeowner_inf3 = {
        "token" : register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : -1,
    }
    removeowner_resp5 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf3)
    assert removeowner_resp5.status_code == 400
    requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf)
    removeowner_inf4 = {
        "token" : register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    removeowner_resp6 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf4)
    assert removeowner_resp6.status_code == 400
    removeowner_inf5 = {
        "token" : register[1]['token'],
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    removeowner_resp7 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf5)
    assert removeowner_resp7.status_code == 400
    # channel_id is valid and the authorised user does not have owner permissions in the channel
    removeowner_inf6 = {
        "token" : '-1',
        "channel_id" : channel[1]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    removeowner_resp8 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf6)
    assert removeowner_resp8.status_code == 403

def test_channel_removeowner2(register, channel):
    # test for AccessError when:
    #    channel_id is valid and the authorised user does not have owner permissions in the channel
    addowner_inf = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    requests.post(config.url + 'channel/addowner/v1', json = addowner_inf)
    removeowner_inf = {
        "token" : register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    removeowner_resp = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf)
    assert removeowner_resp.status_code == 403
    join_inf = {
        "token": register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
    }
    requests.post(config.url + 'channel/join/v2', json = join_inf)
    addowner_inf2 = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[2]['auth_user_id'],
    }
    requests.post(config.url + 'channel/addowner/v1', json = addowner_inf2)
    removeowner_inf2 = {
        "token" : register[2]['token'],
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[0]['auth_user_id'],
    }
    requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf2)
    removeowner_inf3 = {
        "token" : register[0]['token'],
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    removeowner_resp1 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf3)
    assert removeowner_resp1.status_code == 200
    removeowner_inf4 = {
        "token" : '-1',
        "channel_id" : channel[0]['channel_id'],
        "u_id" : register[1]['auth_user_id'],
    }
    removeowner_resp2 = requests.post(config.url + 'channel/removeowner/v1', json = removeowner_inf4)
    assert removeowner_resp2.status_code == 403