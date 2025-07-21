# Пишем код создания БД, пишем код создания и наполнения двух таблиц
# Реализован код автоматического создания БД.
# Реализован код для создания таблиц в БД.
# Создается таблица для организаций.
# Создается таблица для вакансий.
# FK
# employeers <-> vacancies
# CREAT IF NOT EXISTS
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

# Загрузка переменных из .env файла
load_dotenv()

# Получение параметров из .env файла параметры подключения к БД
DB_USER = os.getenv("DB_USER", "default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "hh_vacancies")

# SQL-запросы для создания БД и таблиц
CREATE_DB_QUERY = f"CREATE DATABASE {DB_NAME}"

CREATE_TABLE_VACANCIES_QUERY = """
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    vacancy_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    company_name VARCHAR(500),
    company_id INTEGER REFERENCES companies(id),
    salary_from INTEGER,
    salary_to INTEGER,
    currency VARCHAR(10),
    area VARCHAR(255),
    description TEXT,
    url VARCHAR(255)
)
"""

CREATE_TABLE_COMPANIES_QUERY = """
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    website VARCHAR(255),
    logo_url VARCHAR(255),
    description TEXT
)
"""


def create_connection() -> object:
    """Создание подключения к PostgreSQL"""
    connection = None
    try:
        # Сначала создаем базовое соединение
        connection = psycopg2.connect(
            database="postgres",  # Для создания новой БД используем postgres
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
        )

        # Затем включаем autocommit
        connection.autocommit = True

        print("Соединение с PostgreSQL установлено")
    except OperationalError as e:
        print(f"Ошибка при подключении к PostgreSQL: {e}")
    return connection


def create_database(connection) -> None:
    """Создание новой базы данных с проверкой существования"""
    try:
        with connection.cursor() as cursor:
            # Проверяем существование БД
            cursor.execute(
                f"""
            SELECT 1 
            FROM pg_database 
            WHERE datname = '{DB_NAME}'
            """
            )
            if cursor.fetchone():
                print(f"База данных {DB_NAME} уже существует")
                return

            # Если БД не существует, создаем её
            cursor.execute(CREATE_DB_QUERY)
            print(f"База данных {DB_NAME} создана успешно")
    except OperationalError as e:
        print(f"Ошибка при создании БД: {e}")


def create_tables(connection) -> None:
    """Создание таблиц в БД"""
    try:
        with connection.cursor() as cursor:
            # Создаем таблицу компаний
            cursor.execute(CREATE_TABLE_COMPANIES_QUERY)
            # Создаем таблицу вакансий
            cursor.execute(CREATE_TABLE_VACANCIES_QUERY)
            connection.commit()
            print("Таблицы созданы успешно")
    except OperationalError as e:
        print(f"Ошибка при создании таблиц: {e}")


def insert_company(connection, company) -> None:
    """Вставка компании в таблицу"""
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO companies (
                company_id, name, website, logo_url, description
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING
            """
            cursor.execute(
                query,
                (
                    company["company_id"],
                    company["name"],
                    company.get("website", ""),
                    company.get("logo_url", ""),
                    company.get("description", ""),
                ),
            )
            connection.commit()
    except OperationalError as e:
        print(f"Ошибка при вставке данных о компании: {e}")


def insert_vacancy(connection, vacancy) -> None:
    """Вставка вакансии в таблицу"""
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO vacancies (
                vacancy_id, name, company_name, company_id, salary_from, salary_to,
                currency, area, description, url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
            """
            cursor.execute(
                query,
                (
                    vacancy.get("vacancy_id"),
                    vacancy.get("name"),
                    vacancy.get("company_name"),
                    vacancy.get("company_id"),  # Теперь используем company_id вместо company_name
                    vacancy.get("salary_from"),
                    vacancy.get("salary_to"),
                    vacancy.get("currency"),
                    vacancy.get("area"),
                    vacancy.get("description"),
                    vacancy.get("url"),
                ),
            )
            connection.commit()
    except OperationalError as e:
        print(f"Ошибка при вставке данных: {e}")


def main() -> None:
    """
    функция инициализации системы,
    которая настраивает базу данных и
    добавляет примерные данные для демонстрации работы приложения.
    """
    # Создаем подключение к PostgreSQL
    connection = create_connection()

    if connection is not None:
        try:
            # Создаем новую БД
            create_database(connection)
            connection.close()  # Закрываем старое соединение

            # Переключаемся на созданную БД
            connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
            connection.autocommit = True  # Включаем autocommit здесь

            # Создаем таблицы
            create_tables(connection)

            # Пример данных для демонстрации
            sample_company = {
                "company_id": "comp123",
                "name": 'ООО "Рога и Копыта"',
                "website": "https://company.ru",
                "logo_url": "https://logo.png",
                "employee_count": "100-500",
                "description": "Описание компании",
            }

            # Сначала вставляем компанию
            insert_company(connection, sample_company)

            # Получаем ID вставленной компании
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id FROM companies 
                    WHERE company_id = %s
                """,
                    (sample_company["company_id"],),
                )
                company_db_id = cursor.fetchone()[0]

            sample_vacancy = {
                "vacancy_id": "vac123",
                "name": "Python Developer",
                "company_id": company_db_id,  # Используем полученный ID
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "area": "Москва",
                "description": "Описание вакансии",
                "url": "https://vacancy.ru",
            }

            # Теперь можно вставить вакансию
            insert_vacancy(connection, sample_vacancy)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            if connection:
                connection.close()


if __name__ == "__main__":
    main()
