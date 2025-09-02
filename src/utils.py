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
                                id int PRIMARY KEY,
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

    # Собираем все вакансии
    for employer in employers:
        vacancies = hh_parser.get_vacancies_by_employer_id(employer["id"])
        for vacancy in vacancies:
            # Добавляем employer_id в каждую вакансию
            vacancy["employer_id"] = employer["id"]  # ← Вот это важно!
            all_vacancies.append(vacancy)

    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for vacancy in all_vacancies:
                try:
                    cur.execute("""
                        INSERT INTO vacancies (id, name, employer_id, salary_from, salary_to, url) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["employer_id"],  # ← Теперь здесь будет значение
                        vacancy.get("salary_from", 0),
                        vacancy.get("salary_to", 0),
                        vacancy.get("url", "")
                    ))
                except Exception as e:
                    print(f"Ошибка при вставке вакансии {vacancy['id']}: {e}")

        conn.commit()