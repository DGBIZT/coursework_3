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
                    'name': company_name,
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

                # company_name = list(company_vacancies.keys())[0] Начать с этого момента разбор NULL в столбце
                # for vacancy in company_vacancies[company_name]:
                # Обрабатываем каждую вакансию
                for vacancy in company_vacancies:


                    # Проверяем наличие зарплаты
                    salary_info = vacancy.get('salary', {})
                    if vacancy.get('salary') is not None:
                        salary_from = vacancy['salary'].get('from', 0)
                        salary_to = vacancy['salary'].get('to', 0)
                        salary_currency = vacancy['salary'].get('currency', 'Не указано')
                    else:
                        salary_from = 0
                        salary_to = 0
                        salary_currency = 'Не указано'

                    # company_name = (
                    #     vacancy.get('employer', {}).get('name')
                    #     if vacancy.get('employer')
                    #     else list(company_vacancies.keys())[0] # получаем название компании из верхнего уровня
                    #
                    #     if company_vacancies
                    #     else 'Нет информации'
                    # )

                    sample_vacancy = {
                        'vacancy_id': vacancy.get('id', 'N/A'), # id Вакансия
                        'name': vacancy.get('name', 'Нет названия'), # Наименование вакансии
                        'company_name': vacancy.get('employer', {}).get('name'), # Наименование компании
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
