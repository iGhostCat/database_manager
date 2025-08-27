import pytest
from src.vacancy import Vacancy


class TestVacancy:
    def test_vacancy_creation(self):
        """Тест создания вакансии."""
        vacancy = Vacancy(
            name="Python Developer",
            link="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000},
            description="Разработка на Python"
        )
        assert vacancy.name == "Python Developer"
        assert vacancy.link == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000

    def test_salary_validation_none(self):
        """Тест валидации зарплаты, если salary=None."""
        vacancy = Vacancy(
            name="Python Dev",
            link="https://hh.ru/vacancy/456",
            salary=None,
            description="No salary info"
        )
        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 0

    def test_from_dict(self):
        """Тест создания вакансии из словаря."""
        vacancy_data = {
            "name": "Backend Developer",
            "link": "https://hh.ru/vacancy/789",
            "salary": {"from": 120000, "to": None},
            "description": "Django/Flask"
        }
        vacancy = Vacancy.from_dict(vacancy_data)
        assert vacancy.name == "Backend Developer"
        assert vacancy.salary_from == 120000
        assert vacancy.salary_to == 0