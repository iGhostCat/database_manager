from src.utils import create_tables, create_database, insert_employers, insert_vacancies
from src.db_manager import DB_Manager


db_name = "course5"
create_database(db_name)
create_tables(db_name)
insert_employers(db_name)
insert_vacancies(db_name)

db_manager = DB_Manager(db_name)
print (db_manager.all_employers())
print (db_manager.vacancies_from_selected_employers())