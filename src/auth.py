import re
import smtplib
import random
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from src.data_store import data_store
from src.error import InputError
from src.other import *
from src.config import *


REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

# login function check valid password
def auth_login_v2(email, password):
    store = data_store.get()

    # set a loop to locate email address
    counter = 0
    while counter < len(store['users']):
        if store['users'][counter]['email'] == email:
            if store['users'][counter]['password'] != hash(password):
                raise InputError("Wrong Password")
            else:
                break
        counter += 1

    # unenroll email cannot login
    if counter == len(store['users']):
        raise InputError("Unregistered Email")

    # create a input dictionary
    user_info = {}
    user_info['u_id'] = store['users'][counter]['auth_user_id']
    user_info['session_id'] = generate_new_session_id()
    token = encode_jwt(user_info)
    store['token'].append(token)
    data_store.set(store)

    return {
        'token': token,
        'auth_user_id': store['users'][counter]['auth_user_id'],
    }

# register one user with valid information
def auth_register_v2(email, password, name_first, name_last):
    store = data_store.get()
    permission_id = 2
    # check if permission_id
    if store['users'] == []:
        permission_id = 1

    # check email is valid or not
    check_valid_email(email)
    # check name is valid or not
    check_valid_name(name_first, name_last)
    # test for valid password
    if len(password) < 6:
        raise InputError("Too Short Password")

    new_auth_user_id = len(store['users']) + 1

    handle = str.lower(name_first) + str.lower(name_last)
    handle = ''.join(filter(str.isalnum, handle))

    if len(handle) > 20:
        handle = handle[0:20]

    # if name is used, then add a number as suffix
    counter = 0
    handle_suffix = -1
    while counter < len(store['users']):
        # pseudo_handle based on users' name
        pseudo_handle_first = str.lower(store['users'][counter]['name_first'])
        pseudo_handle_last = str.lower(store['users'][counter]['name_last'])
        pseudo_handle = pseudo_handle_first + pseudo_handle_last
        pseudo_handle = ''.join(filter(str.isalnum, pseudo_handle))
        # take each username into account
        if handle == pseudo_handle:
            handle_suffix += 1
        counter += 1

    if handle_suffix >= 0:
        double_check_handle = handle + str(handle_suffix)
        for each_user in store['users']:
            if each_user['handle'] == double_check_handle:
                handle_suffix += 1
        handle += str(handle_suffix)

    time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    if store['users'] == []:
        store['channels_exist'].append({'num_channels_exist' : 0, 'time_stamp': time})
        store['dms_exist'].append({'num_dms_exist' : 0, 'time_stamp': time})
        store['messages_exist'].append({'num_messages_exist' : 0, 'time_stamp': time})
    store['users'].append({
        'auth_user_id': new_auth_user_id,
        'email': email,
        'password': hash(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'permission_id': permission_id,
        'removed': False,
        'reset_code': '',
        'profile_img_url': default_image_address,
        'channels_joined': [{'num_channels_joined': 0, 'time_stamp': time}],
        'dms_joined': [{'num_dms_joined': 0, 'time_stamp': time}],
        'messages_sent': [{'num_messages_sent': 0, 'time_stamp': time}]
    })
    # when register, login this user
    data_store.set(store)
    token = auth_login_v2(email, password)['token']
    return {
        'token': token,
        'auth_user_id': new_auth_user_id,
    }

# logout user who already login
def auth_logout_v1(token):
    store = data_store.get()
    # cheak whether valid token
    check_valid_token(token, store['token'])
    store['token'].remove(token)
    data_store.set(store)
    return {}

# request to reset password
def auth_passwordreset_request_v1(email):
    store = data_store.get()
    # generate a random number as reset_code and encode
    reset_code = str(random.randint(100000, 999999))
    user_reset_code = encode_password_or_reset_code(reset_code)
    # search for target email and store reset_code
    user_infomation = {}
    for each_user in store['users']:
        if each_user['email'] == email:
            each_user['reset_code'] = user_reset_code
            user_infomation['u_id'] = each_user['auth_user_id']
            user_infomation['name'] = each_user['handle']
    # index is zero means there is no email matched
    if user_infomation == {}:
        return {}
    # if matchs
    send_email(email, reset_code, user_infomation['name'])
    # logout after sending email
    target_token = ''
    for each_token in store['token']:
        if user_infomation['u_id'] == decode_jwt(each_token)['u_id']:
            target_token = each_token
    store['token'].remove(target_token)
    data_store.set(store)
    return {}

# reset password
def auth_passwordreset_reset_v1(reset_code, new_password):
    if len(new_password) < 6:
        raise InputError('Too Short Password')
    store = data_store.get()
    for each_user in store['users']:
        if each_user['reset_code'] == '':
            continue
        else:
            if reset_code == decode_password_or_reset_code(each_user['reset_code']):
                each_user['password'] = hash(new_password)
                data_store.set(store)
                return {}
    raise InputError('Invalid Reset_code')


# helper function
# check email whether valid
def check_valid_email(email):
    store = data_store.get()
    # test for the format of e-mail
    if not re.fullmatch(REGEX, email):
        raise InputError("Invalid Email")
    # test this email is whether been used or not
    for user in store['users']:
        if email == user['email']:
            raise InputError("Used Email")

# check name whether valid
def check_valid_name(name_first, name_last):
    # test for valid name
    if not 1 <= len(name_first) <= 50:
        raise InputError("Invalid First_name")
    if not 1 <= len(name_last) <= 50:
        raise InputError("Invalid Last_name")

# send email to given address
def send_email(email, reset_code, name):
    # cannot check email whether valid
    mail_content = f'''
                    <h1>
                        Hello Dear {name}!<br>
                        How are you today ?
                    </h1>
                    <hr>
                    <h2>
                        We've detected someone trying to change your password.<br>
                        Please make sure it is your own operation.<br>
                        Your reset code is <strong>{reset_code}</strong>.<br>
                        Please don't tell this code to others.<br>
                        Hope you successfully reset your password.<br>
                        <img src = 'cid:image_R'>
                    </h2>
                    <hr>
                    <h3>
                        Thank you.<br><br>
                        Best regards,<br>
                        W17B_EAGLE
                    </h3>
                    '''
    # the mail addresses and password
    sender_address = 'secretmark2021@gmail.com'
    sender_pass = 'uptdwrcuwaedhrre'
    receiver_address = email
    # setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Reset Password'
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    file_image = open(r'image_email/R.jpg', 'rb')
    data_image = file_image.read()
    file_image.close()
    image = MIMEImage(data_image)
    image.add_header('Content-ID', '<image_R>')
    message.attach(image)
    # create SMTP session for sending the mail and use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # enable security
    session.starttls()
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return
