import sqlite3


def create_database():
    # Подключаемся к базе данных (или создаем ее, если не существует)
    conn = sqlite3.connect('messages.db')

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Создаем таблицу для хранения сообщений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT NOT NULL,
        message_send_id TEXT NOT NULL,
        UNIQUE (message_id, message_send_id)
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


# Функция для добавления сообщения
def add_message(message, message_send):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    try:
        # Добавляем сообщение в таблицу
        cursor.execute("INSERT INTO messages (message_id, message_send_id) VALUES (?, ?)", (message, message_send))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Ошибка: Сообщение с таким содержимым '{message}' и '{message_send}' уже существует.")
    finally:
        conn.close()


def get_message_by_id(message_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    try:
        # Получаем сообщение по ID
        cursor.execute("SELECT * FROM messages WHERE message_id=?", (message_id,))
        result = cursor.fetchone()

        if result:
            return result[2]  # Возвращаем message_send_id
        else:
            return None  # Если message_id не найден
    finally:
        # Закрываем соединение
        conn.close()





# conn = sqlite3.connect('messages.db')
# cursor = conn.cursor()
# message_id ='afzwo5ftyigj8gsndmef9ic8ja'
# # Получаем сообщение по ID
# cursor.execute("SELECT * FROM messages WHERE message_id=?", (message_id,))
# message = cursor.fetchall()
# print(message)

# Закрываем соединение
# conn.close()

