import os
from abc import ABC, abstractmethod

import requests as requests
from dotenv import load_dotenv

load_dotenv()


class ApiLoad(ABC):
    @abstractmethod
    def __init__(self, job_title):
        pass


class HhLoad(ApiLoad):
    def __init__(self,job_title):
        self.api_url = "https://api.hh.ru/vacancies"
        self.job_title = job_title
        self.options = {'per_page': 100,
                        'text': self.job_title,
                        'search_field': 'name',
                        'area': 1,
                        'only_with_salary': True}

    def get_job(self):
        response = requests.get(self.api_url, params=self.options)
        print(response.json())


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
        print(response.json())

