from abc import ABC, abstractmethod
import requests
from requests import JSONDecodeError

from settings import HH_URL
from src.exeptions import HeadHunterAPIException


class API(ABC):
    """
    Абстрактный класс
    """

    @abstractmethod
    def load_vacancies(self, *args) -> list[dict]:
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        self.__url = HH_URL
        self.__params = {'text': '', 'search_field': 'name', 'page': 0, 'per_page': 100}

    def load_vacancies(self, user_keyword: str) -> list[dict]:
        """
        Получение списка вакансий в формате json
        """
        vacancies = []
        self.__params['text'] = user_keyword

        response = requests.get(self.__url, params=self.__params)
        is_allowed = self.__check_status(response)
        if not is_allowed:
            raise HeadHunterAPIException(f'Ошибка заброса данных:{response.status_code}, {response.text} ')
        try:
            while self.__params.get('page') != response.json()['pages']:
                response = requests.get(self.__url, params=self.__params)
                vacancy = response.json()['items']
                vacancies.extend(vacancy)
                self.__params['page'] += 1
        except JSONDecodeError:
            raise HeadHunterAPIException(f'Ошибка получения данных JSON: {response.text}')

        return vacancies

    @staticmethod
    def __check_status(response) -> bool:
        """"
        Проверка статуса запроса url
        """
        return response.status_code == 200
