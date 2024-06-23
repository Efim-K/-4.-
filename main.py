import logging

from src.exeptions import APIException
from src.utils import user_interaction

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        user_interaction()
    except APIException as e:
        logger.exception(f'Ошибка обращения к HeadHunterAPI. {e}')
        print('Сервис не доступен')
