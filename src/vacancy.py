
class Vacancy:

    def __init__(self, name, link, salary, description):
        self.name = name
        self.link = link
        self.salary = salary
        self.__validate(salary)
        self.description = description


    def __validate(self, salary):
        if salary:
            self.salary_from = salary['from'] if salary['from'] else 0
            self.salary_to = salary['to'] if salary['to'] else 0
        else:
            self.salary_from = 0
            self.salary_to = 0

    def __lt__(self, other):
        '''Знак меньше <'''
        return self.salary_from < other.salary_from

    def __repr__(self):
        return f"Vacancy({self.name}, {self.link}, {self.salary}, {self.description})"

    @classmethod
    def from_dict(cls, vacancy_dict):
        """Создаёт объект Vacancy из словаря."""
        return cls(
            name=vacancy_dict.get('name', 'Без названия'),
            link=vacancy_dict.get('link', 'Нет ссылки'),
            salary=vacancy_dict.get('salary', {'from': 0, 'to': 0}),
            description=vacancy_dict.get('description', 'Нет описания')
        )
