from time_messenger import Driver
import requests
import json


def bot_login(bot_pass, url):

    bot = Driver({'token': bot_pass, 'port': 443, 'url': url, 'scheme': "https"})
    login_result = bot.login()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bot_pass
    }

    return bot,  headers


def send_to_time(channel_id, message, headers, url):

    payload = {
        'channel_id': channel_id,
        'message': message
    }

    response = requests.post('https://' + url + '/api/v4/posts', json=payload, headers=headers)
    return response


def send_to_time_root(channel_id, message, headers, url,root):

    payload = {
        'channel_id': channel_id,
        'message': message,
        'root_id': root
    }

    response = requests.post('https://' + url + '/api/v4/posts', json=payload, headers=headers)
    return response


def sender_time(direct_channel_id, message, bot_pass, url, root=None):
    bot, headers = bot_login(bot_pass, url)

    try:
        if root is None:
            info_message = send_to_time(direct_channel_id, message, headers, url)
        else:
            info_message = send_to_time_root(direct_channel_id, message, headers, url,root)
        event = info_message.json()
        print('Успешно отправили сообщение')
    except:
        print(f'Что-то не так с отправкой ')
    return event['id']


def update_message(direct_channel_id, message, bot_pass, url, post_id):
    bot, headers = bot_login(bot_pass, url)
    payload = {
        'id': post_id,
        'message': message,
    }

    try:
        response = requests.put('https://' + url + '/api/v4/posts/'+post_id, json=payload, headers=headers)

        print('Успешно отправили сообщение')
    except:
        print(f'Что-то не так с отправкой ')


