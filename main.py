from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.hh_api import HH_API

from typing import List
def dialog_query():
    """Получение поискового запроса от пользователя и выгрузка вакансий"""
    print("🔎 Поиск вакансий на hh.ru")
    search_query = input("Введите поисковый запрос (например, 'Python'): ").strip()
    pages_to_load = int(input("Сколько страниц загрузить (1-5)? ").strip() or 1)

    # 1. Получаем вакансии через API
    hh_api = HH_API()
    vacancies_data = hh_api.get_vacancies(search_query, pages_to_load)

    # 2. Сохраняем в JSON
    saver = JSONSaver('../data/vacancies.json')
    saver.write_vacancies(vacancies_data)
    print(f"✅ Найдено и сохранено {len(vacancies_data)} вакансий.")

    # 3. Загружаем из JSON в виде объектов Vacancy
    vacancies = saver.read_vacancies()
    return vacancies

def top_n_vacs(vacancies):
    try:
        n = int(input("Сколько вакансий показать? ").strip())
        sorted_vacancies = sorted(
            vacancies,
            key=lambda v: (v.salary_from + v.salary_to) / 2 if v.salary_to else v.salary_from,
            reverse=True
        )
        print(f"\n🔝 Топ-{n} вакансий по зарплате:")
        for i, vacancy in enumerate(sorted_vacancies[:n], 1):
            print(f"{i}. {vacancy.name}")
            print(f"   💰 Зарплата: {vacancy.salary_from} – {vacancy.salary_to}")
            print(f"   🔗 Ссылка: {vacancy.link}\n")
    except ValueError:
        print("❌ Нужно ввести число!")

def search_by_keyword(vacancies):
    keyword = input("Введите ключевое слово для поиска: ").strip().lower()
    found_vacancies = [
        v for v in vacancies
        if v.description and keyword in v.description.lower()
    ]
    print(f"\n🔍 Найдено {len(found_vacancies)} вакансий с '{keyword}':")
    for i, vacancy in enumerate(found_vacancies, 1):
        print(f"{i}. {vacancy.name}")
        print(f"   📝 Описание: {vacancy.description[:100]}...")
        print(f"   🔗 Ссылка: {vacancy.link}\n")

def main():
    """Консольный интерфейс для работы с вакансиями hh.ru."""

    vacancies = dialog_query()
    while True:
        print("\n🔹 Доступные действия:")
        print("1. Показать топ N вакансий по зарплате")
        print("2. Найти вакансии по ключевому слову в описании")
        print("3. Выход")

        choice = input("Выберите действие (1/2/3): ").strip()

        # 1. Топ N вакансий по зарплате
        if choice == "1":
           top_n_vacs(vacancies)

        # 2. Поиск по ключевому слову в описании
        elif choice == "2":
            search_by_keyword(vacancies)

        # 3. Выход
        elif choice == "3":
            print("👋 До свидания!")
            break

        else:
            print("❌ Неверный ввод. Попробуйте снова.")



main()
'''hh = HH_API()
vacancies = hh.get_vacancies('python', 1)
json_saver = JSONSaver()
json_saver.write_vacancies(vacancies)'''