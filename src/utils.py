import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    logger.debug(f"Вызов load_operations с путем: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден по пути: {file_path}")
            return []

        file_size = os.path.getsize(file_path)
        logger.debug(f"Размер файла {file_path}: {file_size} байт")

        if file_size == 0:
            logger.error(f"Файл пустой: {file_path}")
            return []

        logger.info(f"Начало чтения файла: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.debug(f"Прочитано {len(content)} символов из файла")

            if not content.strip():
                logger.error(f"Файл содержит только пробельные символы: {file_path}")
                return []

            try:
                data = json.loads(content)
            except json.JSONDecodeError as json_error:
                logger.error(f"Ошибка парсинга JSON в файле {file_path}: {str(json_error)}")
                logger.debug(f"Содержимое файла (первые 500 символов): {content[:500]}")
                return []

        if not isinstance(data, list):
            logger.error(f"JSON не является списком. Тип данных: {type(data)}")
            logger.debug(f"Содержимое JSON: {str(data)[:500]}")
            return []

        operations_count = len(data)

        valid_operations = 0
        for i, operation in enumerate(data):
            if not isinstance(operation, dict):
                logger.warning(f"Операция {i} не является словарем: {type(operation)}")
            elif not operation.get("id"):
                logger.warning(f"Операция {i} не имеет ID")
            else:
                valid_operations += 1

        # Логирование результата
        logger.info(f"Успешно загружено {operations_count} операций из {file_path}")
        logger.debug(f"Валидных операций: {valid_operations}")

        if operations_count > 0 and valid_operations < operations_count:
            logger.warning(
                f"Некоторые операции имеют невалидный формат: {operations_count - valid_operations} из {operations_count}"
            )

        return data

    except PermissionError as e:
        logger.error(f"Нет прав на чтение файла {file_path}: {str(e)}")
        return []
    except OSError as e:
        logger.error(f"Ошибка ОС при работе с файлом {file_path}: {str(e)}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Ошибка декодирования файла {file_path}: {str(e)}")
        return []
    except MemoryError as e:
        logger.error(f"Недостаточно памяти для загрузки файла {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {str(e)}", exc_info=True)
        return []
