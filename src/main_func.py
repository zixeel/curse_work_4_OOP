from src.api_cls import *
from src.json_cls import JSONSaver

platforms = ["HeadHunter", "SuperJob"]
VACANCY_FILE = 'vacancies.json'


def main():
    """Функция интерфейса пользователя"""
    try:
        while True:
            # Пользователь выбирает платформу и делает запрос по вакансиям
            user_input = input('Введите название платформы. Если захотите выйти введите "exit"\n').lower()
            if user_input.lower() == 'exit':
                exit()
            user_vacancy = input('Введите поисковый запрос:\n')
            if user_input == platforms[0].lower():
                platform = HhLoad(user_vacancy)
                hh_vacancies = platform.get_job()
                if len(hh_vacancies) == 0:
                    print('Нет вакансий по вашему запросу')
                    continue
                vacancies = get_from_headhunter(hh_vacancies)
                break
            elif user_input == platforms[1].lower():
                platform = SuperJobLoad(user_vacancy)
                sj_vacancies = platform.get_job()
                if len(sj_vacancies) == 0:
                    print('Нет вакансий по вашему запросу')
                    continue
                vacancies = get_from_superjob(sj_vacancies)
                break
            else:
                print('Такой платформы нет в базе')

        while True:
            # Пользователь фильтрует вакансии по требованиям
            filter_words = input("Введите ключевые слова для фильтрации вакансий:\n").lower()
            if filter_words == 'exit':
                exit()
            filtered_vacancies = filter_vacancies(vacancies, filter_words.split())
            if len(filtered_vacancies) == 0:
                print('Нет вакансий по данным критериям, введите другие критерии или "exit" для выхода')
            else:
                break

        # Вакансии выводятся в топ N и сохраняются в JSON файл
        while True:
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N.\n"))
            except ValueError:
                print('"N" должно быть целым числом')
                continue
            else:
                top = get_top_vacancies(filtered_vacancies, top_n)
                for vacancy in top:
                    JSONSaver(VACANCY_FILE).add_vacancy(vacancy)
                    print(vacancy)
                break

    except Exception as e:
        raise e


def filter_vacancies(vacancies: list, filter_words: list):
    """Функция для фильтрации вакансий по критериям"""
    filtered_list = []
    for vacancy in vacancies:
        for word in filter_words:
            if word in vacancy.requirement.lower().split():
                filtered_list.append(vacancy)
    return filtered_list


def get_top_vacancies(vacancies_list: list, top_number: int):
    """Функция для получения топ N вакансий"""
    return sorted(vacancies_list)[:top_number]


def get_from_headhunter(vacancies: list):
    """Функция для инициализации вакансий с платформы HeadHunter"""
    vacancies_list = []
    for item in vacancies:
        if item['snippet']['requirement']:
            if item['salary']['to']:
                if item['salary']['currency'] == 'RUR':
                    vacancy = Vacancy(item['name'], item['alternate_url'], item['salary']['to'],
                                      item['snippet']['requirement'])
                    vacancies_list.append(vacancy)
    return vacancies_list


def get_from_superjob(vacancies: list):
    """Функция для инициализации вакансий с платформы SuperJob"""
    vacancies_list = []
    for item in vacancies:
        if item['candidat']:
            if item['payment_to']:
                if item['currency'] == 'rub':
                    vacancy = Vacancy(item['profession'], item['link'], item['payment_to'],
                                      item['candidat'])
                    vacancies_list.append(vacancy)
    return vacancies_list