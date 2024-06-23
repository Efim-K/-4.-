import logging
from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH.joinpath('data')
FILE_PATH_JSON = DATA_PATH.joinpath('vacancies.json')
FILE_PATH_SELECT = DATA_PATH.joinpath('vacancies_select.json')
HH_URL = 'https://api.hh.ru/vacancies'
