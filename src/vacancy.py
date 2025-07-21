import requests
from .other_module import companies

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
    # print(vacancies_data)
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