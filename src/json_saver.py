from abc import ABC, abstractmethod
from typing import List

from src.vacancy import Vacancy

import json

class AbsJSON(ABC):
    @abstractmethod
    def write_vacancies(self, vacancies: list[dict]):
        pass

    @abstractmethod
    def read_vacancies(self):
        pass

    @abstractmethod
    def delete_vacancies(self):
        pass


class JSONSaver(AbsJSON):

    def __init__(self, filepath ='../data/vacancies.json'):
        self.__filepath = filepath

    def write_vacancies(self, vacancies: list[dict]):
        vacancies_filter = []
        for vacancy in vacancies:
            # Проверяем наличие salary
            salary = vacancy.get("salary")
            if salary:
                salary_from = salary.get("from") if salary.get("from") is not None else 0
                salary_to = salary.get("to") if salary.get("to") is not None else 0
            else:
                salary_from = 0
                salary_to = 0

            # Проверяем наличие description
            snippet = vacancy.get("snippet", {})
            description = snippet.get("requirement") if snippet else "Нет описания"

            vacancies_filter.append({
                "name": vacancy.get("name", "Без названия"),
                "link": vacancy.get("alternate_url", "Нет ссылки"),
                "salary": {"from": salary_from, "to": salary_to},
                "description": description
            })

        with open(self.__filepath, "w", encoding="utf-8") as file:
            json.dump(vacancies_filter, file, ensure_ascii=False, indent=4)

    def read_vacancies(self) -> List[Vacancy]:
        """Читает вакансии из JSON-файла и возвращает список объектов Vacancy."""
        try:
            with open(self.__filepath, "r", encoding="utf-8") as file:
                vacancies_data = json.load(file)
                return [Vacancy.from_dict(v) for v in vacancies_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Если файла нет или он пуст → возвращаем пустой список

    def delete_vacancies(self):
        """Очищает файл с вакансиями."""
        with open(self.__filepath, "w", encoding="utf-8") as file:
            file.write("[]")  # Записываем пустой список
