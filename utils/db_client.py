import psycopg2
from psycopg2 import extras

from resources.db_creds import DBCreds


def connect_to_postgres():
    """Функция для подключения к PostgreSQL базе данных"""
    connection = None
    cursor = None
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            dbname=DBCreds.DB_MOVIES_NAME,
            user=DBCreds.USERNAME,
            password=DBCreds.PASSWORD,
            host=DBCreds.DB_MOVIES_HOST,
            port=DBCreds.DB_MOVIES_PORT
        )

        print("Подключение успешно установлено")


        # Вывод информации о PostgreSQL сервере
        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")
        return connection, cursor

    except Exception as error:
        print("Ошибка при работе с PostgreSQL:", error)
        return None

"""connection, cursor = connect_to_postgres()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Выполнение SQL-запроса
cursor.execute('''
SELECT * from genres
ORDER by id desc limit 100'''
)

        # Получение результата
record = cursor.fetchall()
print(record)"""