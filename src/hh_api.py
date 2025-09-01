
import requests

class HH_Parser:
    def get_employers(self):
        ''' Метод для соединения с HH.ru и получения списка работодателей '''
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers/", params = params)
        response.raise_for_status()
        data = response.json()["items"]
        employers = []
        for employer in data:
            employers.append({"id": employer["id"], "name": employer["name"]})
        return employers


    def get_vacancies_by_employer_id(self, employer_id):
        params = {"employer_id": employer_id, "per_page": 50}
        response = requests.get('https://api.hh.ru/vacancies', params = params)
        response.raise_for_status()
        data = response.json()["items"]
        salary_from = 0
        salary_to = 0
        vacancies = []
        for vacancy in data:
            if data["salary"]:
                if data["salary"]["from"] and data["salary"]["to"] :
                    salary_from = data["salary"]["from"]
                    salary_to = data["salary"]["to"]
                elif data["salary"]["from"] and not data["salary"]["to"]:
                    salary_from = data["salary"]["from"]
                    salary_to = salary_from
                elif data["salary"]["to"] and not data["salary"]["from"]:
                    salary_to = data["salary"]["to"]
                    salary_from = salary_to
                else:
                    salary_from = 0
                    salary_to = 0
            vacancies.append({"id": data["id", "name": data["name"], "salary_from": salary_from, "salary_to": salary_to, "url": data["alternate_url"]]})

        return vacancies




if __name__ == '__main__':
    hh = HH_Parser()
    #print(hh.get_employers())
    print(hh.get_vacancies_by_employer_id(1942330))