import json
import os
from abc import ABC, abstractmethod

import requests as requests
from dotenv import load_dotenv

load_dotenv()


class UrlError(Exception):
    """Класс ошибки в URL адресе"""

    def __init__(self, msg):
        super.__init__(msg)


class ApiLoad(ABC):
    @abstractmethod
    def __init__(self, job_title):
        pass


class HhLoad(ApiLoad):
    def __init__(self, job_title):
        self.api_url = "https://api.hh.ru/vacancies"
        self.job_title = job_title
        self.options = {'per_page': 100,
                        'text': self.job_title,
                        'search_field': 'name',
                        'area': 1,
                        'only_with_salary': True}

    def get_job(self):
        response = requests.get(self.api_url, params=self.options)
        return response.json()['items']


class SuperJobLoad(ApiLoad):
    def __init__(self, job_title):
        self.api_url = 'https://api.superjob.ru/2.0/vacancies/'
        self.job_title = job_title
        self.headers = {'X-Api-App-Id': os.getenv('SUPER_JOB_API')}
        self.options = {'keyword': self.job_title,
                        'count': 100,
                        'town': 4}

    def get_job(self):
        response = requests.get(self.api_url, params=self.options, headers=self.headers)
        return response.json()['objects']


class Vacancy:
    """Класс, который позволяет создавать экземпляры вакансий и осуществлять с ними работу"""
    __slots__ = {'name', 'url', 'salary', 'requirement'}

    def __init__(self, name: str, url: str, salary: int, requirement: str):
        self.name = name
        if not isinstance(self.name, str):
            raise TypeError("Название вакансии должно быть типа 'str'")
        self.url = url
        if self.url[:8] != 'https://':
            raise UrlError("Ссылка должна начинаться с https://")
        self.salary = salary
        if self.salary is None:
            raise AttributeError('Поле не может быть пустым')
        self.requirement = requirement
        if self.requirement is None:
            raise AttributeError('Поле не может быть пустым')

    def __str__(self):
        return f'Название вакансии - {self.name}\n' \
               f'Ссылка - {self.url}\n' \
               f'З/п до {self.salary} RUR\n' \
               f'Требования - {self.requirement}\n'

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary
