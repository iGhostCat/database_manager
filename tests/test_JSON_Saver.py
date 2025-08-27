import pytest
import os
import json
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    @pytest.fixture
    def saver(self, tmp_path):
        """Фикстура: создает временный файл для тестов."""
        test_file = tmp_path / "test_vacancies.json"
        return JSONSaver(test_file)

    def test_write_and_read_vacancies(self, saver, tmp_path):
        """Тест записи и чтения вакансий."""
        test_vacancies = [
            {
                "name": "Python Dev",
                "link": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000},
                "description": "Python coding"
            }
        ]
        saver.write_vacancies(test_vacancies)

        # Проверяем, что файл создан
        assert os.path.exists(saver._JSONSaver__filepath)

        # Читаем вакансии и проверяем данные
        vacancies = saver.read_vacancies()
        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Dev"

    def test_delete_vacancies(self, saver):
        """Тест очистки файла с вакансиями."""
        test_vacancies = [{"name": "Test", "link": "test", "salary": None, "description": "Test"}]
        saver.write_vacancies(test_vacancies)
        saver.delete_vacancies()

        # Проверяем, что файл пуст
        with open(saver._JSONSaver__filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert data == []