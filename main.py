# Код для создания БД вызывается в основном скрипте программы.
# Код для создания таблиц в БД вызывается в основном скрипте программы.

import psycopg2
from psycopg2 import sql, OperationalError
import os
from dotenv import load_dotenv
from src.utils import create_connection, create_database, create_tables, insert_company, insert_vacancy
from src.hh_api import get_company_info, get_company_vacancies


def main():
    load_dotenv()

    # Параметры подключения к БД
    DB_USER = os.getenv('DB_USER', 'default_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'hh_vacancies')

    # Создаем подключение к PostgreSQL
    connection = create_connection()

    if connection is not None:
        try:
            # Создаем новую БД
            create_database(connection)
            connection.close()  # Закрываем старое соединение

            # Переключаемся на созданную БД
            connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST
            )
            connection.autocommit = True

            # Создаем таблицы
            create_tables(connection)

            # Получаем информацию о компаниях
            hh_company = get_company_info()

            # Обрабатываем каждую компанию
            for company_name, data in hh_company.items():
                # Безопасное получение логотипа
                logo_urls = data.get('logo_urls')
                if logo_urls:
                    logo_url = logo_urls.get('original', 'Нет логотипа')
                else:
                    logo_url = 'Нет логотипа'

                # Формируем данные компании
                sample_company = {
                    'company_id': data.get('id', 'N/A'),
                    'company_name': company_name,
                    'website': data.get('alternate_url', 'N/A'),
                    'logo_url': logo_url,
                    'description': data.get('description', 'Описание отсутствует').strip()
                }

                # Вставляем компанию в БД
                insert_company(connection, sample_company)

                # Получаем ID вставленной компании
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT id FROM companies 
                        WHERE company_id = %s
                    """, (sample_company['company_id'],))
                    company_db_id = cursor.fetchone()[0]

                # Получаем вакансии компании
                # Получаем все вакансии для компании
                all_company_vacancies = get_company_vacancies()

                # Получаем только вакансии для текущей компании
                company_vacancies = all_company_vacancies.get(company_name, [])

                # Обрабатываем каждую вакансию
                for vacancy in company_vacancies:


                    # Проверяем наличие зарплаты
                    salary_info = vacancy.get('salary', {})
                    if vacancy.get('salary') is not None:
                        salary_from = vacancy['salary'].get('from', 'Не указано')
                        salary_to = vacancy['salary'].get('to', 'Не указано')
                        salary_currency = vacancy['salary'].get('currency', 'Не указано')
                    else:
                        salary_from = 'Не указано'
                        salary_to = 'Не указано'
                        salary_currency = 'Не указано'

                    sample_vacancy = {
                        'vacancy_id': vacancy.get('id', 'N/A'), # id Вакансия
                        'name': vacancy.get('name', 'Нет названия'), # Наименование вакансии
                        'company_name': vacancy.get('employer', {}).get('name', 'Нет информации'), # Наименование компании
                        'company_id': company_db_id,  # Используем полученный ID
                        'salary_from': salary_from, # Заработная плата от
                        'salary_to': salary_to, # Заработная плата до
                        'currency': salary_currency, # Валюта
                        'area': vacancy.get('area', {}).get('name', 'Нет информации'), # Область
                        'description': vacancy.get('snippet', {}).get('requirement', 'описание отсутствует'), # Описание вакансии
                        'url': vacancy.get('alternate_url', "Нет URL") # Ссылка
                    }

                    # Вставляем вакансию в БД
                    insert_vacancy(connection, sample_vacancy)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            connection.rollback()  # Откатываем изменения при ошибке
        finally:
            if connection:
                connection.close()

if __name__ == '__main__':
    main()
# import psycopg2
# from psycopg2 import sql, OperationalError
# import os
# from dotenv import load_dotenv
# from src.utils import create_connection, create_database, create_tables, insert_company, insert_vacancy
# from src.hh_api import get_company_info, get_company_vacancies
#
# def main():
#
#     load_dotenv()
#     # Получение параметров из .env файла параметры подключения к БД
#     DB_USER = os.getenv('DB_USER', 'default_user')
#     DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
#     DB_HOST = os.getenv('DB_HOST', 'localhost')
#     DB_NAME = os.getenv('DB_NAME', 'hh_vacancies')
#
#     # Создаем подключение к PostgreSQL
#     connection = create_connection()
#
#     if connection is not None:
#         try:
#             # Создаем новую БД
#             create_database(connection)
#             connection.close()  # Закрываем старое соединение
#
#             # Переключаемся на созданную БД
#             connection = psycopg2.connect(
#                 database=DB_NAME,
#                 user=DB_USER,
#                 password=DB_PASSWORD,
#                 host=DB_HOST
#             )
#             connection.autocommit = True  # Включаем autocommit здесь
#
#             # Создаем таблицы
#             create_tables(connection)
#
#             hh_company = get_company_info()
#             for company_name, data in hh_company.items():
#                 # Безопасное получение логотипа
#                 logo_urls = data.get('logo_urls')
#                 if logo_urls:
#                     logo_url = logo_urls.get('original', 'Нет логотипа')
#                 else:
#                     logo_url = 'Нет логотипа'
#                 sample_company = {
#                     'company_id': data.get('id', 'N/A'),
#                     'company_name': company_name,
#                     'website': data.get('alternate_url', 'N/A'),
#                     'logo_url': logo_url,
#                     'description': data.get('description', 'Описание отсутствует').strip()
#                 }
#
#             # # Пример данных для демонстрации
#             # sample_company = {
#             #     'company_id': 'comp123',
#             #     'name': 'ООО "Рога и Копыта"',
#             #     'website': 'https://company.ru',
#             #     'logo_url': 'https://logo.png',
#             #     'employee_count': '100-500',
#             #     'description': 'Описание компании'
#             # }
#
#             # Сначала вставляем компанию
#             insert_company(connection, sample_company)
#
#             # Получаем ID вставленной компании
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT id FROM companies
#                     WHERE company_id = %s
#                 """, (sample_company['company_id'],))
#                 company_db_id = cursor.fetchone()[0]
#
#             hh_vacancy = get_company_vacancies()
#             for vacancy, data in hh_vacancy.items():
#
#                 sample_vacancy ={
#                     'vacancy_id': data.get('id', 'N/A'),
#                     'name': data.get('name', 'Нет названия'),
#                     'company_id': company_db_id,  # Используем полученный ID
#                     'salary_from': data.get('salary_from', 'N/A'),
#                     'salary_to': data.get('salary_to', 'N/A'),
#                     'area': data.get('area', {}).get('name', 'Нет информации'),
#                     'description':data.get('snippet', {}).get('requirement', 'описание отсутствует'),
#                     'url': data.get('alternate_url', "Нет URL")
#                 }
#             # sample_vacancy = {
#             #     'vacancy_id': 'vac123',
#             #     'name': 'Python Developer',
#             #     'company_name': 'Школа хобби',
#             #     'company_id': company_db_id,  # Используем полученный ID
#             #     'salary_from': 100000,
#             #     'salary_to': 150000,
#             #     'currency': 'RUB',
#             #     'area': 'Москва',
#             #     'description': 'Описание вакансии',
#             #     'url': 'https://vacancy.ru'
#             # }
#
#             # Теперь можно вставить вакансию
#             insert_vacancy(connection, sample_vacancy)
#
#         except Exception as e:
#             print(f"Произошла ошибка: {e}")
#         finally:
#             if connection:
#                 connection.close()
#
# if __name__ == '__main__':
#     main()