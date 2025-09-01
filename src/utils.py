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
            cur.execute("CREATE TABLE employers ("
                        "id int PRIMARY KEY,"
                        "name varchar(255) NOT NULL,")
    conn.close()
        #Второй запрос для создания таблицы вакансий

def insert_employers(db_name):
    params = config()
    hh_parser = HH_Parser()
    employers = hh_parser.get_employers()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s)", (employer["id"], employer["name"] ))
    conn.close()