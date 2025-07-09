# Пишем подключение к БД

import psycopg2

#connect to db
conn = psycopg2.connect(
    host = 'localhost',
    database = 'postgres', # Подключаемся к системной базе
    user = 'postgres',
    password = 'your_password',
)

# # create cursor
# cur = conn.cursor()
#
# # execute query
# cur.execute("SELECT * FROM user_account") # пример
#
#
# # close cursor and connection
# cur.close()
# conn.close()

'''
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError

def create_database():
    try:
        # Подключение к стандартной базе postgres
        connection = psycopg2.connect(
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432",
            database="postgres"  # Подключаемся к системной базе
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Создаем новую базу данных
        db_name = "my_database"
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name)
        ))
        
        print(f"База данных {db_name} успешно создана")
        
    except OperationalError as e:
        print(f"Ошибка при создании БД: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
Настройка подключения
В коде необходимо заменить:

your_password на пароль от пользователя postgres

my_database на желаемое имя создаваемой базы данных

Создание таблиц
После создания БД можно добавить функцию создания таблиц:

def create_tables():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432",
            database="my_database"  # Теперь подключаемся к созданной БД
        )
        
        cursor = connection.cursor()
        
        # Создаем таблицу users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE
            )
        """)
        
        print("Таблицы успешно созданы")
        
    except OperationalError as e:
        print(f"Ошибка при создании таблиц: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
Запуск скрипта
Создайте новый проект в PyCharm

Создайте файл с расширением .py

Вставьте код

Запустите скрипт'''