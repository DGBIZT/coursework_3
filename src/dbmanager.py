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

    def execute_query(self, query, params=None):
        """
        Выполнение SQL-запроса
        :param query: SQL-запрос
        :param params: параметры запроса
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)

    def close(self):
        """
        Закрытие соединения с БД
        """
        if self.connection:
            self.connection.close()
            print("Соединение с БД Закрыто")

        # метод подключения к БД (cur, conn)

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return: список кортежей (название компании, количество вакансий)
        """
        query = """
        SELECT 
            companies.name, 
            COUNT(vacancies.id) as vacancies_count
        FROM 
            vacancies
        LEFT JOIN 
            companies ON vacancies.company_id = companies.id
        GROUP BY 
            companies.id
        ORDER BY 
            vacancies_count DESC
        """

        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

                # Формируем список словарей для более удобного использования
                companies = []
                for row in results:
                    company_dict = {
                        'company_name': row[0],
                        'vacancies_count': row[1]
                    }
                    companies.append(company_dict)

                return companies

        except Exception as e:
            print(f"Произошла ошибка при получении данных: {e}")
            return []

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию
        :return: список словарей с информацией о вакансиях
        """
        query = """
        SELECT 
            companies.name AS company_name,
            vacancies.name AS vacancy_name,
            vacancies.salary_from,
			vacancies.salary_to,
            vacancies.url
        FROM 
            vacancies
        LEFT JOIN 
            companies ON vacancies.company_id = companies.id
        ORDER BY 
            company_name
        """

        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

                # Формируем список словарей
                # Создаем пустой список для хранения вакансий
                vacancies = []

                # Проходим по каждой строке в результатах запроса
                for row in results:
                    # Создаем словарь для текущей вакансии
                    vacancy = {
                        'company_name': row[0],
                        'vacancy_name': row[1],
                        'salary': row[2],
                        'url': row[4]
                    }

                    # Добавляем словарь в общий список
                    vacancies.append(vacancy)

                return vacancies

        except Exception as e:
            print(f"Произошла ошибка при получении данных: {e}")
            return []

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по всем вакансиям
        :return: среднее значение зарплаты
        """
        query = """
        SELECT 
            AVG(salary_from) AS average_salary
        FROM 
            vacancies
        WHERE 
            salary_from IS NOT NULL
        """

        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()

                # Проверяем, есть ли данные
                if result and result[0] is not None:
                    return float(result[0])
                else:
                    return 0.0

        except Exception as e:
            print(f"Произошла ошибка при получении средней зарплаты: {e}")
            return 0.0

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: список словарей с информацией о вакансиях
        """
        query = """
        SELECT 
            companies.name AS company_name,
            vacancies.name AS vacancy_name,
            vacancies.salary_from,
            vacancies.url
        FROM 
            vacancies
        LEFT JOIN 
            companies ON vacancies.company_id = companies.id
        WHERE 
            vacancies.salary_from > (
                SELECT AVG(salary_from) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL
            )
        ORDER BY 
            vacancies.salary_from DESC
        """

        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

                # Формируем список словарей
                # Создаем пустой список для хранения вакансий
                high_salary_vacancies = []

                # Проходим по каждой строке из результатов
                for row in results:
                    # Создаем словарь с понятными названиями полей
                    vacancy_info = {
                        'company_name': row[0],  # название компании
                        'vacancy_name': row[1],  # название вакансии
                        'salary': row[2],  # зарплата
                        'url': row[3]  # ссылка на вакансию
                    }

                    # Добавляем созданный словарь в общий список
                    high_salary_vacancies.append(vacancy_info)

                return high_salary_vacancies

        except Exception as e:
            print(f"Произошла ошибка при получении данных: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова
        :param keyword: строка с искомым словом/фразой
        :return: список словарей с информацией о подходящих вакансиях
        """
        # Используем ILIKE для регистронезависимого поиска
        query = """
        SELECT 
            companies.name AS company_name,
            vacancies.name AS vacancy_name,
            vacancies.salary_from,
            vacancies.url
        FROM 
            vacancies
        LEFT JOIN 
            companies ON vacancies.company_id = companies.id
        WHERE 
            vacancies.name ILIKE %s
        ORDER BY 
            company_name
        """

        # Формируем шаблон поиска с подстановочными знаками
        search_pattern = f'%{keyword}%'

        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, (search_pattern,))
                results = cursor.fetchall()

                # Формируем список словарей
                # Создаём пустой список для хранения найденных вакансий
                matching_vacancies = []

                # Проходим по каждой строке из полученных результатов
                for row in results:
                    # Создаём словарь с информацией о вакансии
                    # Берем данные из строки и присваиваем им понятные имена
                    vacancy = {
                        'company_name': row[0],  # название компании
                        'vacancy_name': row[1],  # название вакансии
                        'salary': row[2],  # зарплата
                        'url': row[3]  # ссылка на вакансию
                    }

                    # Добавляем словарь в общий список
                    matching_vacancies.append(vacancy)

                return matching_vacancies

        except Exception as e:
            print(f"Произошла ошибка при поиске вакансий: {e}")
            return []


if __name__ == "__main__":
    # print(f"\n***Список кортежей (название компании, количество вакансий)***")
    # db = DBManager()
    # try:
    #     db.connect()
    #     companies_data = db.get_companies_and_vacancies_count()
    #
    #     # Выводим результаты
    #     for company in companies_data:
    #         print(f"Компания: {company['company_name']}, "
    #               f"Количество вакансий: {company['vacancies_count']}")
    #
    # finally:
    #     db.close()
    # print(f"\n***Список словарей с информацией о вакансиях*** ")
    # db = DBManager()
    # try:
    #     db.connect()
    #     all_vacancies = db.get_all_vacancies()
    #
    #     # Выводим результаты
    #     for vacancy in all_vacancies:
    #         print(f"Компания: {vacancy['company_name']}")
    #         print(f"Вакансия: {vacancy['vacancy_name']}")
    #         print(f"Зарплата: {vacancy['salary']}")
    #         print(f"Ссылка: {vacancy['url']}\n")
    #
    # finally:
    #     db.close()
    #
    # print(f"\n***Среднее значение зарплаты***")
    # db = DBManager()
    # try:
    #     db.connect()
    #     avg_salary = db.get_avg_salary()
    #     print(f"Средняя зарплата по всем вакансиям: {avg_salary:.2f} рублей")
    #
    # finally:
    #     db.close()

    print(f"\n***список словарей с информацией о вакансиях, у которых зарплата выше средней по всем вакансиям***")
    db = DBManager()
    try:
        db.connect()
        high_salary_vacancies = db.get_vacancies_with_higher_salary()

        # Выводим результаты
        for vacancy in high_salary_vacancies:
            print(f"Компания: {vacancy['company_name']}")
            print(f"Вакансия: {vacancy['vacancy_name']}")
            print(f"Зарплата: {vacancy['salary']}")
            print(f"Ссылка: {vacancy['url']}\n")

    finally:
        db.close()
    #
    print(f"\n***список словарей с информацией о подходящих вакансиях с искомым словом/фразой***")
    db = DBManager()
    try:
        db.connect()
        keyword = 'python'  # искомое слово
        matching_vacancies = db.get_vacancies_with_keyword(keyword)

        # Выводим результаты
        for vacancy in matching_vacancies:
            print(f"Компания: {vacancy['company_name']}")
            print(f"Вакансия: {vacancy['vacancy_name']}")
            print(f"Зарплата: {vacancy['salary']}")
            print(f"Ссылка: {vacancy['url']}\n")

    finally:
        db.close()
