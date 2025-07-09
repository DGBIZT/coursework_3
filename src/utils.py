# Пишем код создания БД, пишем код создания и наполнения двух таблиц
# Реализован код автоматического создания БД.
# Реализован код для создания таблиц в БД.
            # Создается таблица для организаций.
            # Создается таблица для вакансий.
                    # FK
                    # employeers <-> vacancies
            # CREAT IF NOT EXISTS

import psycopg2
from psycopg2 import sql, OperationalError
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

 # Получение параметров из .env файла параметры подключения к БД
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'hh_vacancies')

# SQL-запросы для создания БД и таблиц
CREATE_DB_QUERY = f"CREATE DATABASE {DB_NAME}"

CREATE_TABLE_VACANCIES_QUERY = """
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    vacancy_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
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
    employee_count VARCHAR(100),
    description TEXT
)
"""


def create_connection():
    """Создание подключения к PostgreSQL"""
    connection = None
    try:
        connection = psycopg2.connect(
            database="postgres",  # Для создания новой БД используем postgres
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        print("Соединение с PostgreSQL установлено")
    except OperationalError as e:
        print(f"Ошибка при подключении к PostgreSQL: {e}")
    return connection


def create_database(connection):
    """Создание новой базы данных с проверкой существования"""
    try:
        with connection.cursor() as cursor:
            # Проверяем существование БД
            cursor.execute(f"""
            SELECT 1 
            FROM pg_database 
            WHERE datname = '{DB_NAME}'
            """)
            if cursor.fetchone():
                print(f"База данных {DB_NAME} уже существует")
                return

            # Если БД не существует, создаем её
            cursor.execute(CREATE_DB_QUERY)
            print(f"База данных {DB_NAME} создана успешно")
    except OperationalError as e:
        print(f"Ошибка при создании БД: {e}")


def create_tables(connection):
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


def insert_company(connection, company):
    """Вставка компании в таблицу"""
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO companies (
                company_id, name, website, logo_url, employee_count, description
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING
            """
            cursor.execute(query, (
                company['company_id'],
                company['name'],
                company.get('website', ''),
                company.get('logo_url', ''),
                company.get('employee_count', ''),
                company.get('description', '')
            ))
            connection.commit()
    except OperationalError as e:
        print(f"Ошибка при вставке данных о компании: {e}")


def insert_vacancy(connection, vacancy):
    """Вставка вакансии в таблицу"""
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO vacancies (
                vacancy_id, name, company_id, salary_from, salary_to,
                currency, area, description, url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
            """
            cursor.execute(query, (
                vacancy.get('vacancy_id'),
                vacancy.get('name'),
                vacancy.get('company_id'),  # Теперь используем company_id вместо company_name
                vacancy.get('salary_from'),
                vacancy.get('salary_to'),
                vacancy.get('currency'),
                vacancy.get('area'),
                vacancy.get('description'),
                vacancy.get('url')
            ))
            connection.commit()
    except OperationalError as e:
        print(f"Ошибка при вставке данных: {e}")


def main():
    # Создаем подключение к PostgreSQL
    connection = create_connection()

    if connection is not None:
        # Создаем новую БД
        create_database(connection)

        # Переключаемся на созданную БД
        connection.close()
        connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

        # Создаем таблицы
        create_tables(connection)

        # Пример вставки данных
        # Пример данных для демонстрации
        sample_company = {
            'company_id': 'comp123',
            'name': 'ООО "Рога и Копыта"',
            'website': 'https://company.ru',
            'logo_url': 'https://logo.png',
            'employee_count': '100-500',
            'description': 'Описание компании'
        }

        sample_vacancy = {
            'vacancy_id': 'vac123',
            'name': 'Python Developer',
            'company_id': 'comp123',  # Связываем с компанией
            'salary_from': 100000,
            'salary_to': 150000,
            'currency': 'RUB',
            'area': 'Москва',
            'description': 'Описание вакансии',
            'url': 'https://vacancy.ru'
        }

        # Вставляем данные
        insert_company(connection, sample_company)
        insert_vacancy(connection, sample_vacancy)

        connection.close()


if __name__ == "__main__":
    main()





#
#
# def main():
#     # Создаем подключение к PostgreSQL
#     connection = create_connection()
#
#     if connection is not None:
#         # Создаем новую БД
#         create_database(connection)
#
#         # Переключаемся на созданную БД
#         connection.close()
#         connection = psycopg2.connect(
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST
#         )
#
#         # Создаем таблицу
#         create_table(connection)
#
#         # Пример вставки данных
#         # Здесь нужно интегрировать с вашим кодом получения вакансий
#         # Например:
#         # for company in companies:
#         #     vacancies = get_hh_vacancies(company['id'])
#         #     for vacancy in vacancies:
#         #         insert_vacancy(connection, vacancy)
#
#         connection.close()
#
#
# if __name__ == "__main__":
#     main()
#



###############################################################################
# import json
# import os
# from abc import ABC, abstractmethod
# from pathlib import Path
# from typing import Any, Dict, List, NoReturn, Optional, Tuple, Union
#
# import requests
#
#
# class VacancyApi(ABC):
#
#     @abstractmethod
#     def __load_vacancies(self, keyword):
#         pass
#
#     @abstractmethod
#     def file_writer_base(self):
#         pass
#
#
# class FileStorage(ABC):
#     # Абстрактный класс на добавление вакансии add_vacancy,
#     # получение данных из файла по указанным критериям get_vacancies,
#     # удаление информации о вакансиях delete_vacancy
#     @abstractmethod
#     def add_vacancy(self, vacancy_job):
#         pass
#
#     @abstractmethod
#     def get_vacancies(self, criteria):
#         pass
#
#     @abstractmethod
#     def delete_vacancy(self, vacancy_id):
#         pass
#
#
# class HH(VacancyApi):
#     """
#     Класс для работы с API HeadHunter
#     """
#
#     def __init__(self):
#
#         self.__url = "https://api.hh.ru/vacancies"
#         self.__headers = {"User-Agent": "HH-User-Agent"}
#         self.__params = {"text": "", "page": 0, "per_page": 100, "area": "113"}
#         self.__vacancies = []
#
#     def _VacancyApi__load_vacancies(self, keyword: str) -> None:
#         self.__params["text"] = keyword.lower()
#         while self.__params.get("page") < 20:
#             response = requests.get(self.__url, headers=self.__headers, params=self.__params)
#             if response.status_code == 200:
#                 vacancies = response.json()["items"]
#                 self.__vacancies.extend(vacancies)
#                 self.__params["page"] += 1
#                 # Добавляем проверку на количество страниц
#                 if response.json().get("pages") <= self.__params["page"]:
#                     break
#             else:
#                 raise Exception(f"Ошибка при запросе к API: {response.status_code}")
#
#     def get_vacancies(self) -> List[Dict[str, Any]]:
#         return self.__vacancies
#
#     def file_writer_base(self) -> NoReturn:
#         # Создаем директорию data, если она не существует
#         data_dir = Path("data")
#         data_dir.mkdir(parents=True, exist_ok=True)
#
#         # Формируем полный путь к файлу
#         file_path = os.path.join(data_dir, "vacancies.json")
#         try:
#             with open(file_path, "w", encoding="utf-8") as f:
#                 json.dump(self.__vacancies, f, ensure_ascii=False, indent=2)
#         except IOError as e:
#             print(f"Ошибка записи в файл: {e}")
#
#
# class Vacancy:
#     __slots__ = ("name_vacancy", "url_vacancy", "__salary", "town", "snippet")
#     """
#     Класс для работы с вакансиями
#     """
#
#     def __init__(self, data: Dict[str, Any]):
#         self.name_vacancy = data.get("name", "")
#         self.url_vacancy = data.get("alternate_url", "")
#         salary_data = data.get("salary")
#         self.__salary = salary_data.get("from", 0) if salary_data else 0
#         self.town = data.get("area", {}).get("name", "")
#         self.snippet = data.get("snippet", {}).get("requirement", "")
#
#     @property
#     def salary(self) -> Union[int, float]:
#         return self.__salary
#
#     def __str__(self) -> str:
#         return f"{self.name_vacancy} {self.url_vacancy} {self.__salary} {self.town} {self.snippet}"
#
#     def __eq__(self, other: object) -> bool:
#         """__eq__ - equal означает равно"""
#         if isinstance(other, Vacancy):
#             return self.__salary == other.__salary
#         return NotImplemented
#
#     def __ge__(self, other: object) -> bool:
#         """__ge__ - greater than or equal означает больше или равно"""
#         if isinstance(other, Vacancy):
#             return self.__salary >= other.__salary
#         return NotImplemented
#
#     def matches_keywords(self, keywords: List[str]) -> bool:
#         """Фильтрация по ключевым словам"""
#         text = f"{self.name_vacancy.lower()} {self.snippet.lower()}{self.town.lower()}"
#         return any(word in text for word in keywords)
#
#     @staticmethod
#     def top_number(vacancies: List, number: int) -> List:
#         """
#         Возвращает топ N вакансий по зарплате
#         :param vacancies: список объектов Vacancy
#         :param number: количество вакансий для вывода
#         :return: список топ N вакансий
#         """
#         return vacancies[: number + 1]
#
#     @staticmethod
#     def salary_range(vacancies: list, salary_range: Tuple[Union[int, float]]) -> List:
#         """
#         Фильтрует вакансии по указанному диапазону зарплат
#         :param vacancies: список вакансий
#         :param salary_range: кортеж с минимальным и максимальным значением зарплаты (min_salary, max_salary)
#         :return: список подходящих вакансий
#         """
#         # Проверяем корректность входных данных
#         if not isinstance(salary_range, tuple) or len(salary_range) != 2:
#             raise ValueError("Диапазон зарплат должен быть кортежем из двух чисел")
#
#         min_salary, max_salary = salary_range
#         # Проверяем, что оба значения числа
#         if not isinstance(min_salary, (int, float)) or not isinstance(max_salary, (int, float)):
#             raise TypeError("Значения диапазона зарплат должны быть числами")
#
#         # Фильтруем вакансии по диапазону зарплат
#         filtered_vacancies = [
#             vacancy
#             for vacancy in vacancies
#             if (
#                 vacancy.salary is not None  # Проверяем, что зарплата не None
#                 and min_salary <= vacancy.salary <= max_salary
#             )
#         ]
#
#         return filtered_vacancies

#
# class JsonVacancyManager(FileStorage):
#
#     def __init__(self, filename="data/vacancies.json"):
#         self.__filename = filename
#         self.data = []
#
#     def add_vacancy(self, vacancy_job: Dict) -> Optional:
#         """Добавление вакансии"""
#         try:
#             with open(self.__filename, "r+", encoding="utf-8") as file:
#                 try:
#                     data = json.load(file)
#                 except json.JSONDecodeError:
#                     data = []  # Если файл пустой или некорректный JSON, создаем пустой список
#
#                 if vacancy_job not in data:
#                     data.append(vacancy_job)
#
#                     file.seek(0)  # Перемещение указателя файла в начало
#                     file.truncate()  # Очистка файла перед перезаписью
#                     json.dump(data, file)
#                 else:
#                     return "Данная вакансия уже существует"
#         except Exception as e:
#             return f"Произошла ошибка: {str(e)}"
#         return None  # Возвращаем None при успешном выполнении
#
#     def get_vacancies(self, criteria: Dict) -> Optional:
#         """Получение данных из файла по указанным критериям"""
#         try:
#             with open(self.__filename, "r", encoding="utf-8") as file:
#                 data = json.load(file)
#                 result = list()
#                 for v in data:
#                     if criteria(v):
#                         result.append(v)
#                 return result
#         except FileNotFoundError:
#             print("Файл не найден")
#             return []
#         except json.JSONDecodeError:
#             print("Ошибка декодирования JSON")
#             return []
#         except Exception as e:
#             print(f"Произошла ошибка: {str(e)}")
#             return []
#
#     def delete_vacancy(self, vacancy_id: int) -> None:
#         """Удаление вакансии"""
#         try:
#             with open(self.__filename, "r+", encoding="utf-8") as file:
#                 data = json.load(file)
#                 data = [v for v in data if v.get("id") != vacancy_id]
#                 file.seek(0)
#                 file.truncate()
#                 json.dump(data, file, ensure_ascii=False, indent=2)
#         except FileNotFoundError:
#             raise FileNotFoundError("Файл с вакансиями не найден")
#         except Exception as e:
#             raise Exception(f"Произошла ошибка при удалении вакансии: {str(e)}")


# if __name__ == '__main__':
#     vacancies_list = []  # Создаем список для хранения объектов
#
#     hh_parser = HH()
#     hh_parser._VacancyApi__load_vacancies("Водитель")
#     vacancies_data = hh_parser.get_vacancies()
#     hh_parser.file_writer_base()


    # # Создаем объекты и добавляем их в список
    # for vacancy in vacancies_data:
    #     new_vacancy = Vacancy(vacancy)  # Передаем всю вакансию как один параметр
    #     vacancies_list.append(new_vacancy)

#
#
#     # Сортируем список по зарплате
#     sorted_vacancies = sorted(vacancies_list, key=lambda v: v.salary, reverse=True)
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
#
#     # Фильтруем список вакансий
#     filtered_vacancies = []
#     for vacancy in sorted_vacancies:
#         if vacancy.matches_keywords(filter_words):
#             filtered_vacancies.append(vacancy)
#
#     # Выводим отсортированные вакансии
#     for vacancy in filtered_vacancies:
#         print(vacancy)
#         print("-" * 50)  # Разделитель между вакансиями

# for vacancy in vacancies_data:
#     new_vacancy = Vacancy(vacancy)
#     vacancies_list.append(new_vacancy)

# if len(vacancies_list) >= 2:
#     vacancy1_data = vacancies_list[0]
#     vacancy2_data = vacancies_list[1]
#
#     vacancy1 = Vacancy(
#         name_vacancy=vacancy1_data,
#         url_vacancy=vacancy1_data,
#         salary=vacancy1_data.get('salary'),
#         town=vacancy1_data.get('area'),
#         snippet=vacancy1_data
#     )
#     vacancy2 = Vacancy(
#         name_vacancy=vacancy2_data,
#         url_vacancy=vacancy2_data,
#         salary=vacancy2_data.get('salary'),
#         town=vacancy2_data.get('area'),
#         snippet=vacancy2_data
#     )
# #
#     if vacancy1 == vacancy2:
#         print("Зарплаты равны")
#     else:
#         print(f"Зарплаты отличаются:{"\n"} {vacancy1.name_vacancy} {vacancy1.salary}{"\n"}
#         {vacancy2.name_vacancy} {vacancy2.salary}")
#     if vacancy1 >= vacancy2:
#         print(f"Вакансия №1 {vacancy1.name_vacancy} с зарплатой {vacancy1.salary} больше
#         вакансии №2 {vacancy2.name_vacancy} с зарплатой {vacancy2.salary}")
#     else:
#         print(f"Вакансия №2 {vacancy2.name_vacancy} с зарплатой {vacancy2.salary} больше
#         вакансии №1 {vacancy1.name_vacancy} с зарплатой {vacancy1.salary}")
#
# else:
#
#     print("Недостаточно данных для сравнения")
