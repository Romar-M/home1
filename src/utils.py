import json
import os
from typing import List, Dict, Any


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