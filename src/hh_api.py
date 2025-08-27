from abc import ABC, abstractmethod

import requests

class HH_Parser:
    def get_employers(self):
        ''' Метод для соединения с HH.ru и получения списка работодателей '''
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers/", params = params)
        response.raise_for_status()
        return response.json()["items"]


    def get_vacancies_by_employer_id(self, employer_id):
        params = {"employer_id": employer_id, "per_page": 50}
        response = requests.get('https://api.hh.ru/vacancies', params = params)
        response.raise_for_status()
        return response.json()["items"]


if __name__ == '__main__':
    hh = HH_Parser()
    #print(hh.get_employers())
    print(hh.get_vacancies_by_employer_id(1942330))