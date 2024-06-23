class Vacancy:
    """
    Класс обработки вакансии
    """
    __slots__ = ('__pk', '__published_at', '__name', '__alternate_url', '__area', '__currency', '__salary_from',
                 '__salary_to', '__schedule', '__requirement', '__responsibility')

    def __init__(self, __pk, __published_at, __name, __alternate_url, __area, __currency, __salary_from,
                 __salary_to, __schedule, __requirement, __responsibility):
        # Идентификационный номер
        self.__pk = __pk
        # Дата публикации
        self.__published_at = self.validate_field_str(__published_at)
        # Название вакансии
        self.__name = self.validate_field_str(__name)
        # Ссылка на вакансию
        self.__alternate_url = self.validate_field_str(__alternate_url)
        # место работы
        self.__area = self.validate_field_str(__area)
        # Валюта
        self.__currency = self.validate_field_str(__currency)
        # Зарплата "от"
        self.__salary_from = self.validate_salary(__salary_from)
        # Зарплата "до"
        self.__salary_to = self.validate_salary(__salary_to)
        # График работы
        self.__schedule = self.validate_field_str(__schedule)
        # Требования
        self.__requirement = self.validate_field_str(__requirement)
        # Обязанности
        self.__responsibility = self.validate_field_str(__responsibility)

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
        return self.__salary_to > other.__salary_to

    def __lt__(self, other):
        """
        Cравнение зарплат вакансий на меньше
        """
        return self.__salary_to < other.__salary_to

    def __eq__(self, other):
        """
        Cравнение зарплат вакансий на равенство
        """
        return self.__salary_to == other.__salary_to

    def __str__(self) -> str:
        """
        Вывод пользователю информации о вакансии
        """
        salary = f'Зарплата: от {self.__salary_from} до {self.__salary_to} {self.__currency}'
        return (f'Должность: {self.__name}\n'
                f'Дата публикации: {__published_at}\n'
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
        cls(__pk=vacancy_data.get('id'),
            __published_at=vacancy_data.get('published_at'),
            __name=vacancy_data.get('name'),
            __alternate_url=vacancy_data.get('alternate_url'),
            __area=vacancy_data.get('area').get('name'),
            __currency=vacancy_data.get('salary').get('currency'),
            __salary_from=vacancy_data.get("salary").get("from"),
            __salary_to=vacancy_data.get("salary").get("to"),
            __schedule=vacancy_data.get("schedule").get("name"),
            __requirement=vacancy_data.get('snippet').get('requirement'),
            __responsibility=vacancy_data["snippet"]["responsibility"]
            )
