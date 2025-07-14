# класс, который делает запросы на api HH
import requests

companies  = [
    {'name': 'Т-Банк', 'id': 78638},
    {'name': 'СБЕР', 'id': 3529},
    {'name': 'WEECALL', 'id': 3107303},
    {'name': 'Веб Лидер', 'id': 141108},
    {'name': 'МТС', 'id': 3776},
    {'name': 'КубаньПрофиСервис', 'id': 9202177},
    {'name': 'Группа БАС', 'id': 5974204},
    {'name': 'Ерошко Владимир Владиславович', 'id': 10280369},
    {'name': 'Школа хобби MimiDo & магазин Арт Ткани', 'id': 4480863},
    {'name': 'Совкомбанк', 'id': 7944}
]


# def get_hh_employer():
#     """
#     Функция для получения данных с HH employer
#     """
#
#     # URL-адрес API HeadHunter для поиска вакансий
#     __url = "https://api.hh.ru/vacancies?employer_id="
#
#     # Создаем пустой словарь, куда будем складывать результаты
#     vacancies_list = {}
#
#     # Проходим по списку компаний (предполагается, что список companies уже существует)
#     for company in companies:
#         # Берем ID компании из текущего элемента списка
#         company_id = company["id"]
#
#         # Формируем полный URL для запроса
#         full_url = __url + str(company_id)
#
#         # Делаем запрос к API и получаем ответ в формате JSON
#         response = requests.get(full_url).json()
#
#         # Из полученного ответа берем только список вакансий (поле 'items')
#         vacancies = response['items']
#
#         # Сохраняем вакансии в наш словарь, где ключом будет ID компании
#         vacancies_list[company_id] = vacancies
#
#     # Возвращаем итоговый словарь со всеми вакансиями
#     return vacancies_list

# def hh_api():
#     """Функция для получения данных с HH employer"""
#     __url = "https://api.hh.ru/vacancies?employer_id="
#     vacancies_list = {}
#     for i in companies :
#         vacancies_list[i["id"]] = (requests.get(f'{__url}{i['id']}').json()['items'])
#     return vacancies_list


# def get_hh_vacancies(company_id):
#     """Функция для получения данных с HH vacancies"""
#     __url = "https://api.hh.ru/vacancies/"
#     url = f"{__url}?employer_id={company_id}"
#
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             vacancies = []
#
#
#             for vacancy in data.get('items', []):
#                 vacancies.append({
#                     'vacancy_id': vacancy.get('id'),  # id вакансии
#                     'name': vacancy.get('name'),  # Наименование вакансии
#                     'company_name': vacancy.get('employer', {}).get('name'),  # Организация - имя компании
#                     'salary_from': (vacancy.get('salary') or {}).get('from'),  # Зарплата от
#                     'salary_to': (vacancy.get('salary') or {}).get('to'),  # Зарплата до
#                     'currency': (vacancy.get('salary') or {}).get('currency'),  # Валюта
#                     'area': vacancy.get('area', {}).get('name'),  # Область
#                     'description': vacancy.get('description'),  # Описание
#                     'url': vacancy.get('alternate_url'),  # Ссылка вакансии
#                 })
#             return vacancies
#         else:
#             print(f"Ошибка запроса: {response.status_code}")
#             return []
#     except Exception as e:
#         print(f"Произошла ошибка: {str(e)}")
#         return []
def get_company_info():
    base_url = "https://api.hh.ru/employers/"
    company_details = {}

    for company in companies:
        try:
            # Формируем URL для запроса
            url = f"{base_url}{company['id']}"

            # Делаем запрос
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                company_details[company['name']] = data
            else:
                print(f"Ошибка получения данных для {company['name']}: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при получении данных компании {company['name']}: {str(e)}")

    return company_details

def get_company_vacancies():
    # Базовый URL для API HeadHunter
    base_url = "https://api.hh.ru/vacancies?employer_id="

    # Создаем словарь для хранения результатов
    all_vacancies = {}

    # Проходим по каждой компании в списке
    for company in companies:
        # Получаем ID компании
        company_id = company['id']

        # Формируем полный URL для запроса
        full_url = f"{base_url}{company_id}"

        try:
            # Делаем запрос к API
            response = requests.get(full_url)

            # Проверяем успешность запроса
            if response.status_code == 200:
                # Получаем данные в формате JSON
                data = response.json()

                # Сохраняем только список вакансий
                vacancies = data.get('items', [])

                # Добавляем в общий словарь
                all_vacancies[company['name']] = vacancies
            else:
                print(f"Ошибка при получении данных для {company['name']}: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке компании {company['name']}: {str(e)}")

    return all_vacancies


if __name__ == '__main__':
    # company_info = get_company_info()
    # # print(company_info)
    # for company_name, data in company_info.items():
    #     print(f"ID компании: {data.get('id', 'N/A')}")
    #     print(f"\nИнформация о компании: {company_name}")
    #     print(f"Ссылка на работодателя: {data.get('alternate_url', 'N/A')}")
    #     # Безопасное получение логотипа
    #     logo_urls = data.get('logo_urls')
    #     if logo_urls:
    #         logo_url = logo_urls.get('original', 'Нет логотипа')
    #     else:
    #         logo_url = 'Нет логотипа'
    #     print(f"Логотип: {logo_url}")
    #     print(f'Информация: {data.get('description', '')}')
        # print(f"Рейтинг компании: {data.get('employer_rating', {}).get('total_rating', 'Нет рейтинга')}")
        # print(f"Количество отзывов: {data.get('employer_rating', {}).get('reviews_count', 'N/A')}")
        # print(f"Доверенный работодатель: {data.get('trusted', 'Нет')}")
        # print(f"Аккредитованный IT-работодатель: {data.get('accredited_it_employer', 'Нет')}")
        # print("-" * 40)

    # Получаем данные
    vacancies_data = get_company_vacancies()
    print(vacancies_data)
    # Выводим результаты
    for company_name, vacancies in vacancies_data.items():
        print(f"\nВакансии компании {company_name}:")
        for vacancy in vacancies:
            vacancy_id = vacancy.get('id', 'N/A')  # id Вакансия
            vacancy_name = vacancy.get('name', 'Нет названия') # Наименование вакансии
            # Получаем ссылку на работодателя
            # Важно: employer - это отдельный словарь, нужно обращаться к нему правильно
            employer_info = vacancy.get('employer', {})
            snippet_info = vacancy.get('snippet', {})
            employer_url = employer_info.get('alternate_url', 'Ссылка не найдена')
            employer_id = employer_info.get('id', 'id отсутствует')
            employer_name = employer_info.get('name', 'отсутствует')
            if vacancy.get('salary') is not None:
                salary_from = vacancy['salary'].get('from', 'Не указано')
                salary_to = vacancy['salary'].get('to', 'Не указано')
            else:
                salary_from = 'Не указано'
                salary_to = 'Не указано'

            snippet = snippet_info.get('requirement', 'описание отсутствует')
            alternate = vacancy.get('alternate_url', "Нет URL")
            area = vacancy.get('area', {}).get('name', 'Нет информации')

            print(f"- Наименование вакансии: {vacancy_name}")
            print(f"- Город: {area}")
            print(f"- Сылка на вакансию: {alternate}")
            print(f"- id вакансии: {vacancy_id}")
            print(f"- Описание вакансии: {snippet}")
            print(f"- Номер id компании: {employer_id}")
            print(f"- Наименование компании: {employer_name}")
            print(f"- Ссылка компании: {employer_url} ")
            print(f"- Заработная плата от: {salary_from}")
            print(f"- Заработная плата до: {salary_to}\n")






    # Получаем вакансии для конкретной компании
    # company_id = 4480863  # ID Т-Банка
    # vacancies = get_hh_vacancies(company_id)
    #
    # # Выводим результаты
    # for vacancy in vacancies:
    #     print(f"Вакансия: {vacancy['name']}")
    #     print(f"Компания: {vacancy['company_name']}")
    #     print(f"Зарплата: от {vacancy['salary_from']} до {vacancy['salary_to']} {vacancy['currency']}")
    #     print(f"Регион: {vacancy['area']}")
    #     print(f"Описание: {vacancy['description']}")
    #     print(f"Ссылка: {vacancy['url']}\n")

    # company = get_hh_employer()
    # print(company)