import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql, extras
import os
from contextlib import contextmanager


class DBManager:
    def __init__(self):
        """
        # Загружаем переменные окружения из .env файла
        """
        load_dotenv()

        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST", 'localhost')
        self.port = os.getenv("DB_PORT", '5432')
        self.connection = None

    def connect(self):
        """
        Метод для установления соединения с БД
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Подключение к БД установлено")
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к БД: {e}")

    @contextmanager
    def get_cursor(self):
        """
        Контекстный менеджер для работы с курсором
        """
        try:
            with self.connection.cursor() as cursor:
                yield cursor
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connection.rollback() # это метод, который выполняет откат (отмену) всех изменений, сделанных в рамках текущей транзакции базы данных.
            # т.е., последовательность операций, которые либо выполняются полностью, либо не выполняются вообще.

            raise
        finally:
            self.connection.commit()




    def close(self):
        """
        Закрытие соединения с БД
        """
        if self.connection:
            self.connection.close()
            print("Соединение с БД Закрыто")

        # метод подключения к БД (cur, conn)

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании. '''
        pass
    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        pass
    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        pass
    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass