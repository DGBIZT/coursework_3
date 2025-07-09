
# класс, который делает запросы на api HH
import requests

# companies  = [78638, 3529, 3107303, 141108, 3776, 9202177, 5974204, 10280369, 4480863, 7944]
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

def hh_api():
    """Функция для получения данных с HH employer"""
    __url = "https://api.hh.ru/vacancies?employer_id="
    vacancies_list = {}
    for i in companies :
        vacancies_list[i["id"]] = (requests.get(f'{__url}{i['id']}').json()['items'])
    return vacancies_list




def get_hh_vacancies(company_id):
    """Функция для получения данных с HH vacancies"""
    __url = "https://api.hh.ru/vacancies/"
    url = f"{__url}?employer_id={company_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            vacancies = []


            for vacancy in data.get('items', []):
                vacancies.append({
                    'vacancy_id': vacancy.get('id'),  # id вакансии
                    'name': vacancy.get('name'),  # Наименование вакансии
                    'company_name': vacancy.get('employer', {}).get('name'),  # Организация - имя компании
                    'salary_from': (vacancy.get('salary') or {}).get('from'),  # Зарплата от
                    'salary_to': (vacancy.get('salary') or {}).get('to'),  # Зарплата до
                    'currency': (vacancy.get('salary') or {}).get('currency'),  # Валюта
                    'area': vacancy.get('area', {}).get('name'),  # Область
                    'description': vacancy.get('description'),  # Описание
                    'url': vacancy.get('alternate_url'),  # Ссылка вакансии
                })
            return vacancies
        else:
            print(f"Ошибка запроса: {response.status_code}")
            return []
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return []

if __name__ == '__main__':
    # Получаем вакансии для конкретной компании
    company_id = 4480863  # ID Т-Банка
    vacancies = get_hh_vacancies(company_id)

    # Выводим результаты
    for vacancy in vacancies:
        print(f"Вакансия: {vacancy['name']}")
        print(f"Компания: {vacancy['company_name']}")
        print(f"Зарплата: от {vacancy['salary_from']} до {vacancy['salary_to']} {vacancy['currency']}")
        print(f"Регион: {vacancy['area']}")
        print(f"Описание: {vacancy['description']}")
        print(f"Ссылка: {vacancy['url']}\n")

    # print(hh_api())