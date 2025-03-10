import os
import json
from time_messenger import Driver
from send import sender_time, update_message
from dotenv import load_dotenv
from db import add_message, create_database, get_message_by_id
import getpass
import sys
import time
import logging

# Настройка логирования
logging.basicConfig(
    filename='project.log',  # Имя файла для логирования
    level=logging.DEBUG,      # Устанавливаем уровень логирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Формат записей
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN_RECEIVING')
BOT_PASS = os.getenv('BOT_PASS_SEND')
url = 'api-time-ops.tinkoff.ru'
direct_channel_id = 'kwqf11zwujbtfbuu3uhmu847ry'
channel_id = ['yx5fheddjt8xzcio1rhaafci6w', 'q4jh1xsza3gw8gt8yxcr7751xh']


driver_config = {
    # as time-messenger lib does not provide a proper way to pass
    # websocket specific url, we have to set "ws.time.tinkoff.ru"
    # as base url for both WS and HTTP requests
    "url": "api-time.tinkoff.ru",
    "scheme": "https",
    "port": 443,
    "token": BOT_TOKEN,
}


async def event_handler(message):
    event_data = json.loads(message)
    if "event" in event_data and event_data["event"] == "posted":
        post_data = json.loads(event_data["data"]["post"])
        if post_data['channel_id'] in channel_id:
            message_id = post_data['id']
            root_message = post_data['root_id']
            props_message = post_data['props']
            if root_message == '':
                message_sent_id = sender_time(direct_channel_id, post_data['message'], bot_pass=BOT_PASS, url=url,props=props_message)
                add_message(message_id, message_sent_id)
            else:
                result_message_id = get_message_by_id(root_message)
                if result_message_id is not None:
                    message_sent_id = sender_time(direct_channel_id, post_data['message'], bot_pass=BOT_PASS, url=url, props=props_message, root=result_message_id)

    elif "event" in event_data and event_data["event"] == "post_edited":

        post_data = json.loads(event_data["data"]["post"])
        if post_data['channel_id'] in channel_id:
            message_id = post_data['id']
            message = post_data['message']
            props_message = post_data['props']
            result_message_id = get_message_by_id(message_id)
            update_message(direct_channel_id=direct_channel_id, message=message, bot_pass=BOT_PASS, url=url, post_id=result_message_id, props=props_message)


# def password():
#     # Здесь задайте ваши логин и пароль (для простоты примера)
#     correct_password = "drozdov"
#
#
#     # Ввод пароля (с использованием getpass для сокрытия ввода)
#     password = getpass.getpass("Введите пароль: ")
#     correct_password = "drozdov"
#     if password == correct_password:
#         print("Доступ разрешен!")
#         # Здесь можно добавить основную логику вашей программы
#     else:
#         print("Неправильный логин или пароль./nПрограмма закроется через 5 секунд")
#         time.sleep(5)
#         sys.exit()  # Завершает выполнение программы
#     return

def init_websocket_with_reconnect(driver, event_handler):
    while True:
        try:
            # Инициализация вебсокета
            logging.info('Инициализация вебсокет')
            driver.init_websocket(event_handler)
            logging.warning('Сбросился вебсокет')

        except:
            logging.warning(f"Ошибка при подключении к вебсокету")
            time.sleep(1)  # Задержка перед повторной попыткой подключения


if __name__ == "__main__":
    # Создаем базу данных и таблицу
    # password()
    create_database()
    logging.info('Запускаем программу')

    time_driver = Driver(options=driver_config)

    with time_driver:
        time_driver.login()
        logging.info('Логинимся')
        init_websocket_with_reconnect(time_driver, event_handler)
