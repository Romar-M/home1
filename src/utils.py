import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # Настройка file_handler для логгера модуля utils
    file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Настройка file_formatter для логгера модуля utils
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    try:
        if not os.path.exists(file_path):
            return []

        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError, OSError):
        return []