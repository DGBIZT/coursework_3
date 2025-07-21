# класс, который делает запросы на api HH
import requests
from .other_module import companies


def get_company_info() -> dict:
    """
    Получает информацию о компаниях с HeadHunter API
    """
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
                company_details[company["name"]] = data
            else:
                print(f"Ошибка получения данных для {company['name']}: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при получении данных компании {company['name']}: {str(e)}")

    return company_details


if __name__ == "__main__":
    # Получаем данные о компаниях
    company_data = get_company_info()
    # print(company_data)

    # Выводим информацию
    for company_name, details in company_data.items():
        print(f"\nКомпания: {company_name}")
        print(f"ID: {details.get('id')}")
        print(f"Название: {details.get('name')}")
        print(f"Сайт: {details.get('alternate_url')}")
        print(f"Описание: {details.get('description')}")
        print(f"Логотип: {details.get('logo_url')}")
        print("-" * 40)
