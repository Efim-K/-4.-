from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH.joinpath('data')
FILE_PATH_JSON = DATA_PATH.joinpath('vacancies.json')
