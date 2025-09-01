import psycopg2

def create_database(name):
    conn = psycopg2.connect(dbname="postgres")