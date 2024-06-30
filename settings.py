import logging
from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH.joinpath('data')
FILE_PATH_JSON = DATA_PATH.joinpath('vacancies.json')
HH_URL = 'https://api.hh.ru/vacancies'

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='myapp.log', level=logging.INFO, filemode='a', format=FORMAT)
