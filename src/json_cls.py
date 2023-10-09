import os
from abc import ABC, abstractmethod
import json


class JSONError(Exception):
    """Обработка ошибок с JSON файлом"""
    def __init__(self, msg):
        super().__init__(msg)


class Saver(ABC):
    """Абстрактный класс для хранения вокансий в джсон формате"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(Saver):
    """Класс для работы с данными в JSON файле"""

    def __init__(self, filename: str):
        self.filename = filename

    def load_file(self):
        with open(self.filename, encoding='utf-8') as json_file:
            vacancy_list = json.load(json_file)
        return vacancy_list

    def write_file(self, vacancy_list: list):
        with open(self.filename, 'w', encoding='utf-8') as json_file:
            json.dump(vacancy_list, json_file, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        """Метод добавляющий вакансию в JSON файл"""
        data = {'name': vacancy.name, 'url': vacancy.url, 'salary': vacancy.salary,
                'requirement': vacancy.requirement}
        try:
            with open(self.filename, 'a', encoding='utf-8') as file:
                if os.stat(self.filename).st_size == 0:
                    json.dump([data], file, ensure_ascii=False)
                else:
                    data_list = self.load_file()
                    data_list.append(data)
                    self.write_file(data_list)
        except ValueError:
            raise JSONError('Данные в файле повреждены')

    def get_vacancies_by_salary(self, salary: int):
        """Метод, возвращающий вакансию по заданной з/п"""
        try:
            vacancy_list = []
            data_list = self.load_file()
            for item in data_list:
                if item['salary'] >= salary:
                    vacancy_list.append(item)
            return vacancy_list
        except ValueError:
            raise JSONError('Данные в файле повреждены')

    def delete_vacancy(self, vacancy):
        """Метод, удаляющий выбранную вакансию из JSON файла"""
        try:
            data_list = self.load_file()
            for item in data_list:
                if item['url'] == vacancy.url:
                    data_list.remove(item)
            self.write_file(data_list)
        except ValueError:
            raise JSONError('Данные в файле повреждены')
