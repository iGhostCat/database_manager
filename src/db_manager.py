from config import config
import psycopg2

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

    def all_employers(self):
        query = "SELECT * FROM employers"
        return self.__execute_query(query)

    def vacancies_from_selected_employers(self):
        query = "SELECT * FROM vacancies"
        return self.__execute_query(query)