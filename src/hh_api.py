# класс, который делает запросы на api HH
import requests

companies = [
    {"name": "Т-Банк", "id": 78638},
    {"name": "СБЕР", "id": 3529},
    {"name": "WEECALL", "id": 3107303},
    {"name": "Веб Лидер", "id": 141108},
    {"name": "МТС", "id": 3776},
    {"name": "КубаньПрофиСервис", "id": 9202177},
    {"name": "Группа БАС", "id": 5974204},
    {"name": "Ерошко Владимир Владиславович", "id": 10280369},
    {"name": "Школа хобби MimiDo & магазин Арт Ткани", "id": 4480863},
    {"name": "Совкомбанк", "id": 7944},
]


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


def get_company_vacancies() -> dict:
    """
    Получает список вакансий для каждой компании с HeadHunter API
    """
    # Базовый URL для API HeadHunter
    base_url = "https://api.hh.ru/vacancies?employer_id="

    # Создаем словарь для хранения результатов
    all_vacancies = {}

    # Проходим по каждой компании в списке
    for company in companies:
        # Получаем ID компании
        company_id = company["id"]

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
                vacancies = data.get("items", [])

                # Добавляем в общий словарь
                all_vacancies[company["name"]] = vacancies
            else:
                print(f"Ошибка при получении данных для {company['name']}: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке компании {company['name']}: {str(e)}")

    return all_vacancies


if __name__ == "__main__":

    # Получаем данные
    vacancies_data = get_company_vacancies()
    print(vacancies_data)
    # Выводим результаты
    for company_name, vacancies in vacancies_data.items():
        print(f"\nВакансии компании {company_name}:")
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id", "N/A")  # id Вакансия
            vacancy_name = vacancy.get("name", "Нет названия")  # Наименование вакансии
            # Получаем ссылку на работодателя
            # Важно: employer - это отдельный словарь, нужно обращаться к нему правильно
            employer_info = vacancy.get("employer", {})
            snippet_info = vacancy.get("snippet", {})
            employer_url = employer_info.get("alternate_url", "Ссылка не найдена")
            employer_id = employer_info.get("id", "id отсутствует")
            employer_name = employer_info.get("name", "отсутствует")
            if vacancy.get("salary") is not None:
                salary_from = vacancy["salary"].get("from", "Не указано")
                salary_to = vacancy["salary"].get("to", "Не указано")
            else:
                salary_from = "Не указано"
                salary_to = "Не указано"

            snippet = snippet_info.get("requirement", "описание отсутствует")
            alternate = vacancy.get("alternate_url", "Нет URL")
            area = vacancy.get("area", {}).get("name", "Нет информации")

            print(f"- Наименование вакансии: {vacancy_name}")
            print(f"- Город: {area}")
            print(f"- Ссылка на вакансию: {alternate}")
            print(f"- id вакансии: {vacancy_id}")
            print(f"- Описание вакансии: {snippet}")
            print(f"- Номер id компании: {employer_id}")
            print(f"- Наименование компании: {employer_name}")
            print(f"- Ссылка компании: {employer_url} ")
            print(f"- Заработная плата от: {salary_from}")
            print(f"- Заработная плата до: {salary_to}\n")
