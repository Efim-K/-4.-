import json
from abc import ABC, abstractmethod

from settings import FILE_PATH_JSON
from src.class_vacancy import Vacancy
from src.utils import get_vacancies_instances


class VacanciesABC(ABC):

    @abstractmethod
    def read_vacancies(self) -> json:
        pass

    @abstractmethod
    def save_vacancies(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def del_vacancies(self) -> None:
        pass


class WorkFileVacancies(VacanciesABC):
    """
    Чтение и запись данных вакансий в файл, выбранные пользователем
    """

    def read_vacancies(self) -> json:
        """
        Чтение вакансий из файла
        """
        try:
            with open(FILE_PATH_JSON, "r", encoding="utf8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(FILE_PATH_JSON, "w+", encoding="utf8"):
                return []

    def merging_lists_vacancies(self, vacancies: list[Vacancy]) -> list[dict]:
        """
        Объединение данные по вакансиям нового запроса пользователя с предыдущей историей
        """
        # Загрузка старых данных с вакансиями
        old_vacancies = self.read_vacancies()
        # Преобразование списка словарей вакансий в список класса Вакансий
        old_instances = get_vacancies_instances(old_vacancies)
        # Получаем список id, ранее найденных вакансий
        old_ids = [instance.pk for instance in old_instances]
        # Преобразуем новые вакансии из списка типа Вакансий в список из словарей
        all_instances = [vacancy.to_dict() for vacancy in vacancies if vacancy.pk not in old_ids]
        # Объединяем словари
        all_instances.extend(old_vacancies)

        return all_instances

    def save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """
        Добавление вакансий формата JSON в файл
        """
        # Объединение старых данных с  новыми вакансиями
        new_vacancies = self.merging_lists_vacancies(vacancies)

        with open(FILE_PATH_JSON, "w", encoding="utf8") as f:
            json.dump(new_vacancies, f, ensure_ascii=False, indent=4)

    def del_vacancies(self) -> None:
        """
        Удаление данных из файла
        """
        with open(FILE_PATH_JSON, "w"):
            pass
