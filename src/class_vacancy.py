class Vacancy:
    """
    Класс обработки вакансии
    """

    __slots__ = ('__pk', '__published_at', '__name', '__alternate_url', '__area', '__currency',
                 '__salary_from', '__salary_to', '__schedule', '__requirement', '__responsibility')

    def __init__(self, pk, published_at, name, alternate_url, area, currency, salary_from,
                 salary_to, schedule, requirement, responsibility):
        # Идентификационный номер
        self.__pk = pk
        # Дата публикации
        self.__published_at = self.validate_field_str(published_at)
        # Название вакансии
        self.__name = self.validate_field_str(name)
        # Ссылка на вакансию
        self.__alternate_url = self.validate_field_str(alternate_url)
        # место работы
        self.__area = self.validate_field_str(area)
        # Валюта
        self.__currency = self.validate_field_str(currency)
        # Зарплата "от"
        self.__salary_from = self.validate_salary(salary_from)
        # Зарплата "до"
        self.__salary_to = self.validate_salary(salary_to)
        # График работы
        self.__schedule = self.validate_field_str(schedule)
        # Требования
        self.__requirement = self.validate_field_str(requirement)
        # Обязанности
        self.__responsibility = self.validate_field_str(responsibility)

    @property
    def pk(self):
        return self.__pk

    @property
    def name(self):
        return self.__name

    @property
    def currency(self):
        return self.__currency

    @property
    def area(self):
        return self.__area

    @property
    def requirement(self):
        return self.__requirement

    @property
    def responsibility(self):
        return self.__responsibility

    @staticmethod
    def validate_field_str(field):
        """
        Проверка корректности текстовых данных
        """
        return field if field is not None else 'Нет информации'

    @staticmethod
    def validate_salary(salary):
        """
        Проверка корректности данных зарплат
        """
        return salary if isinstance(salary, int) else 0

    def __gt__(self, other):
        """
        Cравнение зарплат вакансий на больше
        """
        return self.__salary_from > other.__salary_from

    def __lt__(self, other):
        """
        Cравнение зарплат вакансий на меньше
        """
        return self.__salary_from < other.__salary_from

    def __eq__(self, other):
        """
        Cравнение зарплат вакансий на равенство
        """
        return self.__salary_from == other.__salary_from

    def __str__(self) -> str:
        """
        Вывод пользователю информации о вакансии
        """
        salary = f'Зарплата: от {self.__salary_from} до {self.__salary_to} {self.__currency}'
        return (f'Должность: {self.__name}\n'
                f'Дата публикации: {self.__published_at}\n'
                f'Ссылка на вакансию: {self.__alternate_url}\n'
                f'Город: {self.__area}\n'
                f'{salary}\n'
                f'График работы: {self.__schedule}\n'
                f'Требования к кандидату: {self.__requirement}\n'
                f'Обязанности: {self.__responsibility}\n\n')

    def __repr__(self):
        """
        Отладочный вывод класса и атрибутов класса
        """
        return (f"""{self.__class__.__name__}
                {self.__pk},
                {self.__published_at},
                {self.__name},
                {self.__alternate_url},
                {self.__area},
                {self.__currency},
                {self.__salary_from},
                {self.__salary_to},
                {self.__schedule},
                {self.__requirement},
                {self.__responsibility}
        """)

    @classmethod
    def create_vacancy(cls, vacancy_data):
        """
        Инициализация класса вакансий
        """
        currency = 'Нет информации'
        vacancy_from = 0
        vacancy_to = 0

        if vacancy_data.get('salary'):
            if vacancy_data.get('salary').get('currency'):
                currency = vacancy_data.get('salary').get('currency')

            if vacancy_data.get('salary').get('from'):
                vacancy_from = vacancy_data.get('salary').get('from')

            if vacancy_data.get('salary').get('to'):
                vacancy_to = vacancy_data.get('salary').get('to')

        return cls(pk=vacancy_data.get('id'),
                   published_at=vacancy_data.get('published_at'),
                   name=vacancy_data.get('name'),
                   alternate_url=vacancy_data.get('alternate_url'),
                   area=vacancy_data.get('area').get('name'),
                   currency=currency,
                   salary_from=vacancy_from,
                   salary_to=vacancy_to,
                   schedule=vacancy_data.get('schedule').get('name'),
                   requirement=vacancy_data.get('snippet').get('requirement'),
                   responsibility=vacancy_data.get('snippet').get('responsibility')
                   )
