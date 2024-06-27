class Vacancy:
    """
    Класс обработки вакансии
    """

    __slots__ = ('_pk', '_published_at', '_name', '_alternate_url', '_area', '_currency',
                 '_salary_from', '_salary_to', '_schedule', '_requirement', '_responsibility')

    def __init__(self, _pk, _published_at, _name, _alternate_url, _area, _currency, _salary_from,
                 _salary_to, _schedule, _requirement, _responsibility):
        # Идентификационный номер
        self._pk = _pk
        # Дата публикации
        self._published_at = self.validate_field_str(_published_at)
        # Название вакансии
        self._name = self.validate_field_str(_name)
        # Ссылка на вакансию
        self._alternate_url = self.validate_field_str(_alternate_url)
        # место работы
        self._area = self.validate_field_str(_area)
        # Валюта
        self._currency = self.validate_field_str(_currency)
        # Зарплата "от"
        self._salary_from = self.validate_salary(_salary_from)
        # Зарплата "до"
        self._salary_to = self.validate_salary(_salary_to)
        # График работы
        self._schedule = self.validate_field_str(_schedule)
        # Требования
        self._requirement = self.validate_field_str(_requirement)
        # Обязанности
        self._responsibility = self.validate_field_str(_responsibility)

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
        return self._salary_from > other._salary_from

    def __lt__(self, other):
        """
        Cравнение зарплат вакансий на меньше
        """
        return self._salary_from < other._salary_from

    def __eq__(self, other):
        """
        Cравнение зарплат вакансий на равенство
        """
        return self._salary_from == other._salary_from

    def __str__(self) -> str:
        """
        Вывод пользователю информации о вакансии
        """
        salary = f'Зарплата: от {self._salary_from} до {self._salary_to} {self._currency}'
        return (f'Должность: {self._name}\n'
                f'Дата публикации: {self._published_at}\n'
                f'Ссылка на вакансию: {self._alternate_url}\n'
                f'Город: {self._area}\n'
                f'{salary}\n'
                f'График работы: {self._schedule}\n'
                f'Требования к кандидату: {self._requirement}\n'
                f'Обязанности: {self._responsibility}\n\n')

    def __repr__(self):
        """
        Отладочный вывод класса и атрибутов класса
        """
        return (f"""{self.__class__.__name__}
                {self._pk},
                {self._published_at},
                {self._name},
                {self._alternate_url},
                {self._area},
                {self._currency},
                {self._salary_from},
                {self._salary_to},
                {self._schedule},
                {self._requirement},
                {self._responsibility}
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

        return cls(_pk=vacancy_data.get('id'),
                   _published_at=vacancy_data.get('published_at'),
                   _name=vacancy_data.get('name'),
                   _alternate_url=vacancy_data.get('alternate_url'),
                   _area=vacancy_data.get('area').get('name'),
                   _currency=currency,
                   _salary_from=vacancy_from,
                   _salary_to=vacancy_to,
                   _schedule=vacancy_data.get('schedule').get('name'),
                   _requirement=vacancy_data.get('snippet').get('requirement'),
                   _responsibility=vacancy_data.get('snippet').get('responsibility')
                   )
