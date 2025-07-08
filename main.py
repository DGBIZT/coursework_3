import requests
import json
import time
import os
import pandas as pd


def get_employers():
    ''' Функция для получения всех работодателей:'''
    employers = []
    req = requests.get('https://api.hh.ru/employers')
    data = req.content.decode()
    count_of_employers = json.loads(data)['found']

    for i in range(1, count_of_employers + 1):
        try:
            req = requests.get(f'https://api.hh.ru/employers/{i}')
            data = req.content.decode()
            js_obj = json.loads(data)
            employers.append([js_obj['id'], js_obj['name']])
            print(f"Обработано: {i}/{count_of_employers}")

            # Пауза для соблюдения ограничений API
            if i % 200 == 0:
                time.sleep(0.2)

        except:
            continue

    return employers




def get_vacancies(employer_id, area_id):
    '''Функция для поиска вакансий конкретного работодателя:'''
    params = {
        'employer_id': employer_id,
        'area': area_id,
        'page': 0,
        'per_page': 100
    }

    all_vacancies = []
    while True:
        req = requests.get('https://api.hh.ru/vacancies', params=params)
        data = req.content.decode()
        js_obj = json.loads(data)

        all_vacancies.extend(js_obj['items'])

        if params['page'] >= js_obj['pages'] - 1:
            break

        params['page'] += 1
        time.sleep(0.2)  # Пауза между запросами

    return all_vacancies

# Получаем список всех работодателей
employers = get_employers()

# Выбираем конкретного работодателя (например, 2ГИС)
employer_id = 64174

# ID России для поиска по всей стране
area_id = 113

# Получаем все вакансии работодателя
vacancies = get_vacancies(employer_id, area_id)

# Сохраняем результаты в Excel
data = []
for vacancy in vacancies:
    # Извлекаем необходимые поля
    data.append({
        'id': vacancy['id'],
        'name': vacancy['name'],
        'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
        'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
        'area': vacancy['area']['name'],
        'employer': vacancy['employer']['name'],
        'url': vacancy['alternate_url']
    })

df = pd.DataFrame(data)
df.to_excel('vacancies.xlsx', index=False)


'''
Пример реализации
import requests
import json

# Ваши учетные данные
CLIENT_ID = 'ваш_client_id'
CLIENT_SECRET = 'ваш_client_secret'

# Получение токена доступа
def get_access_token():
    url = 'https://hh.ru/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    token = response.json().get('access_token')
    return token

# Получение вакансий компании
def get_company_vacancies(company_id, token):
    url = f'https://api.hh.ru/companies/{company_id}/vacancies'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Список интересных компаний
companies = [
    {'name': 'Яндекс', 'id': 143},
    {'name': 'Сбер', 'id': 2293},
    {'name': 'Тинькофф', 'id': 10088},
    {'name': 'Mail.ru Group', 'id': 152},
    {'name': 'VK', 'id': 2789},
    {'name': 'Альфа-Банк', 'id': 1008},
    {'name': 'МТС', 'id': 1009},
    {'name': 'Ростелеком', 'id': 1010},
    {'name': 'Лаборатория Касперского', 'id': 1011},
    {'name': '1С', 'id': 1012}
]

# Основной код
def main():
    token = get_access_token()
    
    for company in companies:
        print(f"\nКомпания: {company['name']}")
        vacancies = get_company_vacancies(company['id'], token)
        
        for vacancy in vacancies['items']:
            print(f"  Вакансия: {vacancy['name']}")
            print(f"  Зарплата: {vacancy.get('salary', {}).get('from')} - {vacancy.get('salary', {}).get('to')} руб.")
            print(f"  Город: {vacancy['area']['name']}")
            print(f"  Ссылка: {vacancy['alternate_url']}\n")

if __name__ == '__main__':
    main()
Объяснение кода
Получение токена - функция get_access_token() получает токен для доступа к API.

Получение вакансий - функция get_company_vacancies() запрашивает данные о вакансиях конкретной компании.

Список компаний - в массиве companies указаны ID и названия выбранных компаний.

Основной код - функция main() объединяет все компоненты и выводит информацию о вакансиях.
'''