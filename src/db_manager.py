from config import config
import psycopg2
from src.hh_api import HH_Parser

class DB_Manager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query):
        params = config()
        with psycopg2.connect(dbname = self.__db_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        Returns:
            list: Список словарей с названием компании и количеством вакансий
        """
        query = """
            SELECT e.name, COUNT(v.id) as vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.id, e.name
            ORDER BY vacancies_count DESC
        """
        params = config()
        with psycopg2.connect(dbname=self.__db_name, **params) as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchall()

                    # Преобразуем результат в список словарей
                    companies = []
                    for row in result:
                        companies.append({
                            'company_name': row[0],
                            'vacancies_count': row[1]
                        })

                    return companies

            except Exception as e:
                print(f"Ошибка при получении данных о компаниях: {e}")
                return []

    def all_employers(self):
        query = "SELECT * FROM employers"
        return self.__execute_query(query)

    def vacancies_from_selected_employers(self):
        query = "SELECT * FROM vacancies"
        return self.__execute_query(query)

    def get_avg_salary(self):
        query_avg_salary_from = 'SELECT AVG(salary_from) AS INTEGER FROM vacancies'
        query_avg_salary_to = 'SELECT AVG(salary_to) AS INTEGER FROM vacancies'

        avg_salary_from = float(self.__execute_query(query_avg_salary_from)[0][0])
        avg_salary_to = float(self.__execute_query(query_avg_salary_to)[0][0])
        avg_salary_total = {"Средняя зарплата от": avg_salary_from,
                            "Средняя зарплата до": avg_salary_to,
                            "Средняя зарплата между от и до": (avg_salary_from+avg_salary_to)/2}
        return avg_salary_total

    def get_vacancies_with_higher_salary(self):
        '''
        query_avg_salary_from = 'SELECT AVG(salary_from) AS INTEGER FROM vacancies'
        query_avg_salary_to = 'SELECT AVG(salary_to) AS INTEGER FROM vacancies'

        avg_salary_from = float(self.__execute_query(query_avg_salary_from)[0][0])
        avg_salary_to = float(self.__execute_query(query_avg_salary_to)[0][0])
        '''


        query = '''SELECT * FROM vacancies
                  WHERE (salary_from+salary_to)/2 > ((SELECT AVG(salary_from) FROM vacancies )+(SELECT AVG(salary_to) FROM vacancies ))/2'''
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        params = config()
        query = f"SELECT * FROM vacancies WHERE name ILIKE '%{keyword}%'"

        with psycopg2.connect(dbname=self.__db_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

