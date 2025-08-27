from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):

    @abstractmethod
    def connect(self, text):
        pass

    @abstractmethod
    def get_vacancies(self, text, multi_page):
        pass


class HH_API(AbstractAPI):
    __slots__ = ['page', 'text', 'multi_page']
    def __init__(self, page = 0):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__params = {'page' : page, 'per_page' : 15}

    def connect(self, text):
        self.__params['text'] = text
        response = requests.get(self.__url, params = self.__params)
        return response

    def get_vacancies(self, text, multi_page=0):
        all_vacancies = []
        for page in range(multi_page + 1):
            self.__params['page'] = page
            response = self.connect(text)
            if response.status_code != 200:
                break  # Прерываем, если запрос не удался
            vacancies = response.json().get('items', [])
            if not vacancies:
                break  # Прерываем, если вакансий нет
            all_vacancies.extend(vacancies)
        return all_vacancies


if __name__ == '__main__':
    hh = HH_API()
    print(hh.get_vacancies('python', 1 ))