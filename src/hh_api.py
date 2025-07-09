
# класс , который делает запросы на api HH
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
    __url = "https://api.hh.ru/vacancies?employer_id="
    vacancies_list = {}
    for i in companies :
        vacancies_list[i["id"]] = (requests.get(f'{__url}{i['id']}').json()['items'])
    return vacancies_list


print(hh_api())