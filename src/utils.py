import psycopg2
from config import config
from src.hh_api import HH_Parser

def create_database(db_name):
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()

def create_tables(db_name):
    params = config()
    with psycopg2.connect(dbname = db_name, **params) as conn:
        with conn.cursor() as cur:
            #Создание таблицы работодателей
            cur.execute("""
                            CREATE TABLE employers (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(255) NOT NULL
                            )
                        """)
            # Второй запрос для создания таблицы вакансий
            cur.execute("""
                            CREATE TABLE vacancies (
                                id int PRIMARY KEY
                                name varchar,
                                employer_id INTEGER REFERENCES employers(id),
                                salary_from int,
                                salary_to int,
                                url varchar
                            )
                        """)
    conn.close()


def insert_employers(db_name):
    params = config()
    hh_parser = HH_Parser()
    employers = hh_parser.get_employers()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s)", (employer["id"], employer["name"] ))
    conn.close()

def insert_vacancies(db_name):
    params = config()
    hh_parser = HH_Parser()
    employers = hh_parser.get_employers()
    all_vacancies = []
    for employer in employers:
        vacancies = hh_parser.get_vacancies_by_employer_id(employer["id"])
        all_vacancies.append(vacancies)
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for vac in all_vacancies:
                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                            (vac["id"],
                             vac["name"],
                             vac["employer_id"],
                             vac["salary_from"],
                             vac["salary_to"],
                             vac["url"]))
    conn.close()