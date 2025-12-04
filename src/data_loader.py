import pandas as pd
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("data_loader")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/data_loader.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def load_transactions_from_csv(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Считывает финансовые операции из CSV-файла.
    Возвращает список словарей или None в случае ошибки.
    """
    logger.info(f"Попытка загрузки транзакций из CSV: {file_path}")
    try:
        df = pd.read_csv(file_path, dtype=object, keep_default_na=False)
        logger.info(f"Успешно загружен CSV. Найдено {len(df)} строк.")

        # Конвертация DataFrame в список словарей
        transactions = df.to_dict("records")
        logger.info(f"Данные преобразованы в {len(transactions)} транзакций.")
        return transactions

    except FileNotFoundError:
        logger.error(f"CSV-файл не найден: {file_path}")
    except pd.errors.EmptyDataError:
        logger.error(f"CSV-файл пуст: {file_path}")
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV файла {file_path}: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV файла {file_path}: {e}")
    return None


def load_transactions_from_excel(file_path: str, sheet_name: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Считывает финансовые операции из Excel-файла (XLSX).
    Поддерживает указание имени листа. Возвращает список словарей или None в случае ошибки.
    """
    logger.info(f"Попытка загрузки транзакций из Excel: {file_path} (лист: {sheet_name})")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=object, keep_default_na=False)
        logger.info(f"Успешно загружен Excel. Найдено {len(df)} строк.")

        transactions = df.to_dict("records")
        logger.info(f"Данные преобразованы в {len(transactions)} транзакций.")
        return transactions

    except FileNotFoundError:
        logger.error(f"Excel-файл не найден: {file_path}")
    except ValueError as e:
        logger.error(f"Ошибка листа или формата Excel файла {file_path}: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel файла {file_path}: {e}")
    return None
