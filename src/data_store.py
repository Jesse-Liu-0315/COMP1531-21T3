import json
'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [
    #     {
    #         'auth_user_id' : 1,
    #         'email' : '123456@qq.com',
    #         'password' : 'Aa4399',
    #         'name_first' : 'kunkun',
    #         'name_last' : 'wuli',
    #         'handle' : 'kunkunwuli',
    #         'permission_id': 1,
    #         'removed': True
    #         'reset_code': '0',
    #         'profile_img_url': 'http://localhost:port/static/x.jpg',
    #         'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #     },
    #     {
    #         'auth_user_id' : 2,
    #         'email' : '789106@qq.com',
    #         'password' : 'Aa7k7k',
    #         'name_first' : 'caicai',
    #         'name_last' : 'wuli',
    #         'handle' : 'caicaiwuli1',
    #         'permission_id': 0,
    #         'removed': False
    #         'reset_code': '0',
    #         'profile_img_url': 'http://localhost:port/static/x.jpg',
    #         'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #     },
    #     {
    #         'auth_user_id' : 3,
    #         'email' : '789106@qq.com',
    #         'password' : 'Aa7k7k',
    #         'name_first' : 'caicai',
    #         'name_last' : 'wuli',
    #         'handle' : 'caicaiwuli2',
    #         'permission_id': 0,
    #         'removed': False
    #         'reset_code': '0',
    #         'profile_img_url': 'http://localhost:port/static/x.jpg',
    #         'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #     },
    #     {
    #         'auth_user_id' : 4,
    #         'email' : '789106@qq.com',
    #         'password' : 'Aa7k7k',
    #         'name_first' : 'caicai',
    #         'name_last' : 'wuli',
    #         'handle' : 'caicaiwuli3',
    #         'permission_id': 0,
    #         'removed': False
    #         'reset_code': '0',
    #         'profile_img_url': 'http://localhost:port/static/x.jpg',
    #         'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #     },
    ],
    'channels': [
    #     {
    #         'name' : 'test channel1',
    #         'channel_id' : 1,
    #         'owner_members' : [
    #             {
    #                 'u_id' : 1,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}, {'num_channels_joined': 1, 'time_stamp': 1636553606.373519}],
    #                 'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #                 'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #             }
    #         ],
    #         'all_members' : [
    #             {
    #                 'u_id' : 1,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}, {'num_channels_joined': 1, 'time_stamp': 1636553606.373519}],
    #                 'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #                 'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #             },
    #             {
    #                 'u_id' : 2,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}, {'num_channels_joined': 1, 'time_stamp': 1636553606.373519}],
    #                 'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #                 'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #             },
    #             {
    #                 'u_id' : 4,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}, {'num_channels_joined': 1, 'time_stamp': 1636553606.373519}],
    #                 'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #                 'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #             }
    #         ],
    #         'is_public' : 1,
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    #     {
    #         'name' : 'test channel2',
    #         'channel_id' : 2,
    #         'owner_members' : [
    #             {
    #                 'u_id' : 2,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1636553505.373519}, {'num_channels_joined': 1, 'time_stamp': 1636553606.373519}, {'num_channels_joined': 0, 'time_stamp': 1636553900.373519}],
    #                 'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1636553505.373519}],
    #                 'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1636553505.373519}]
    #             }
    #         ],
    #         'all_members' : [
    #             {
    #                 'u_id' : 2,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}, {'channel_leave': 1636553800.373519}]
    #             },
    #             {
    #                 'u_id' : 3,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}, {'channel_leave': 1636553800.373519}]
    #             }
    #         ],
    #         'is_public' : 0,
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     }, 
    #     { 
    #         'name' : 'test channe3',
    #         'channel_id' : 3,
    #         'owner' : [
    #             {
    #                 'u_id' : 3,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             }
    #         ],
    #         'all_members' : [
    #             {
    #                 'u_id' : 1,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             },
    #             {
    #                 'u_id' : 4,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             }
    #         ],
    #         'is_public' : 1,
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    #     {
    #         'name' : 'test channel4',
    #         'channel_id' : 4,
    #         'owner' : [
    #             {
    #                 'u_id' : 4,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             }
    #         ],
    #         'all_members' : [
    #             {
    #                 'u_id' : 3,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'kunkun',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             },
    #             {
    #                 'u_id' : 4,
    #                 'email' : '123@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'kunkunwuli',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'channel_join': 1636553697.373519}]
    #             }
    #         ],
    #         'is_public' : 0,
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    ],
    'token': [
    #     'abcde',
    #     'fghig',
    ],
    'dms': [
    #     {
    #         'name': 'kunkunwuli, caicaiwuli1, caicaiwuli2',
    #         'dm_id': 1,
    #         'all_members': [
    #             {
    #                 'u_id': 1,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli1',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg'
    #             },
    #             {   
    #                 'u_id': 2,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli2',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg'
    #             },
    #             {
    #                 'u_id': 3,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli3',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg'
    #             },
    #         ],
    #         'owner': {
    #             'handle_str': 'user',
    #             'u_id': 1
    #         },
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    #     {
    #         'name': 'kunkunwuli, caicaiwuli1, caicaiwuli2',
    #         'dm_id': 2,
    #         'all_members': [
    #             {
    #                 'u_id': 1,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli1',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'dm_join': 1636553697.373519}]
    #             },
    #             {   
    #                 'u_id': 2,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli2',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg',
    #                 'time_stamp': [{'register': 1636553505.373519}, {'dm_join': 1636553697.373519}]
    #             },
            
    #         ],
    #         'owner': {
    #             'u_id': 1,
    #             'email' : '789106@qq.com',
    #             'name_first' : 'caicai',
    #             'name_last' : 'wuli',
    #             'handle_str' : 'caicaiwuli1',
    #             'profile_img_url': 'http://localhost:port/static/x.jpg'
    #         },
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    #     {
    #         'name': 'kunkunwuli, caicaiwuli1, caicaiwuli2',
    #         'dm_id': 3,
    #         'all_members': [
    #             {   
    #                 'u_id': 2,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli2',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg'
    #             },
    #             {
    #                 'u_id': 3,
    #                 'email' : '789106@qq.com',
    #                 'name_first' : 'caicai',
    #                 'name_last' : 'wuli',
    #                 'handle_str' : 'caicaiwuli3',
    #                 'profile_img_url': 'http://localhost:port/static/x.jpg'
    #             },
    #         ],
    #         'owner': {
    #             'u_id': 2,
    #             'email' : '789106@qq.com',
    #             'name_first' : 'caicai',
    #             'name_last' : 'wuli',
    #             'handle_str' : 'caicaiwuli2',
    #             'profile_img_url': 'http://localhost:port/static/x.jpg'
    #         },
    #         'messages' : [
    #             "message_id" : message_id,
    #             "u_id" : auth_user_id,
    #             "message" : message,
    #             "time_created" : int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()),
    #             "reacts" : [
    #                 {
    #                     "react_id" : 1,
    #                     "u_ids" : [],
    #                     "is_this_user_reacted" : False,
    #                 },
    #             ],
    #             "is_pinned" : False,
    #         ],
    #     },
    ],
    'message_id_removed': [],
    'all_notifications': [],
    'channels_exist': [
    #     {'num_channels_exist' : 0, 'time_stamp': 1636553697.373519},
    ],
    'dms_exist': [
    #     {'num_dms_exist' : 0, 'time_stamp': 1636553697.373519},
    ],
    'messages_exist': [
    #     {'num_messages_exist' : 0, 'time_stamp': 1636553697.373519},
    ]
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    '''store data'''
    def __init__(self):
        self.__store = initial_object

    def get(self):
        data = self.__store
        if not data['users'] and not data['channels'] and not data['token'] and not data['dms'] and not data['message_id_removed']:
            self.__store = read_store()
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        save_store(store)
        self.__store = store

def save_store(data):
    with open("data_in_server.json", "w") as f:
        json.dump(data, f)

def read_store():
    with open("data_in_server.json", "r") as f:
        return json.load(f)

print('Loading Datastore...')

global data_store
data_store = Datastore()
