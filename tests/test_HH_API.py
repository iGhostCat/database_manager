import pytest
from unittest.mock import patch, Mock
from src.hh_api import HH_API
import requests

class TestHHAPI:
    @pytest.fixture
    def api(self):
        return HH_API()

    @patch('requests.get')
    def test_connect_success(self, mock_get, api):
        """Тест успешного подключения к API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "1"}]}
        mock_get.return_value = mock_response

        response = api.connect("Python")
        assert response.status_code == 200

    @patch('requests.get')
    def test_get_vacancies(self, mock_get, api):
        """Тест получения вакансий."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "1", "name": "Python Dev"}]}
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("Python", 1)
        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Dev"