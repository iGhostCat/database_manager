from src.utils import create_tables, create_database, insert_employers, insert_vacancies
from src.db_manager import DB_Manager

def print_employers(employers):
      for emp in employers:
            print(f"Компания: {emp['company_name']}")
            print(f"Количество вакансий компании: {emp['vacancies_count']}\n")

def print_vacancies(vacancies):
      for vacancy in vacancies:
            print(f"Вакансия: {vacancy[1]}")
            print(f"Зарплата от: {vacancy[3]}")
            print(f"Зарплата до: {vacancy[4]}")
            print(f"Ссылка на вакансию: {vacancy[5]}\n")

def print_avg_salary(salary):
      print(f"Средняя зарплата от: {salary['Средняя зарплата от']}")
      print(f"Средняя зарплата до: {salary['Средняя зарплата до']}")
      print(f"Средняя зарплата между от и до: {salary["Средняя зарплата между от и до"]}\n")

if __name__ == '__main__':
      db_name = "course5"
      create_database(db_name)
      create_tables(db_name)
      insert_employers(db_name)
      insert_vacancies(db_name)
      db_manager = DB_Manager(db_name)
      while True:
            print("Приветствую! Я ваш ассистент по работе с вакансиями.\n"
                  "Мной были получены актуальные вакансии, с которыми вы можете ознакомиться\n"
                  "1) Получить список работодателей и количества вакансий каждого\n"
                  "2) Получить список всех вакансий с указанием работодателя\n"
                  "3) Вычислить среднюю зарплату по всем полученным вакансиям\n"
                  "4) Показать вакансии, зарплата в которых выше средней по всем вакансиям\n"
                  "5) Найти вакансии по ключевым словам в названии\n"
                  "6) Выйти из программы")
            select_int = int(input("Введите цифру, соответствующую нужному вам действию:\n"))
            if select_int not in range (1,7):
                  print("Неверный ввод варианта действия")
                  continue
            elif select_int == 1:
                  print_employers(db_manager.get_companies_and_vacancies_count())
            elif select_int == 2:
                  print_vacancies((db_manager.all_vacancies()))
            elif select_int == 3:
                  print_avg_salary(db_manager.get_avg_salary())
            elif select_int == 4:
                  print_vacancies(db_manager.get_vacancies_with_higher_salary())
            elif select_int == 5:
                  query = str(input("Введите ключевые слова для поиска:  "))
                  print_vacancies(db_manager.get_vacancies_with_keyword(query))
            elif select_int == 6:
                  print("Работа завершена. До скорых встреч!")
                  break
      '''
      
      '''

