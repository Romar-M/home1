import os
import requests
from typing import Dict, Any


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> float:
    """
    Получает текущий курс валюты через внешнее API.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API ключ не найден в переменных окружения")

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"

    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Ошибка API запроса. Код статуса: {response.status_code}")

        data = response.json()

        if not data.get("success", True):
            error_info = data.get("error", {}).get("info", "Неизвестная ошибка")
            raise Exception(f"Ошибка API: {error_info}")

        rates = data.get("rates", {})
        if to_currency not in rates:
            raise Exception(f"Курс обмена для валюты {to_currency} не найден")

        return rates[to_currency]

    except requests.exceptions.Timeout:
        raise Exception("Таймаут при запросе к API. Превышено время ожидания")
    except requests.exceptions.ConnectionError:
        raise Exception("Ошибка подключения к API. Проверьте интернет-соединение")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при выполнении запроса: {str(e)}")


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """
    try:
        if not isinstance(transaction, dict):
            raise ValueError("Транзакция должна быть словарем")

        operation_amount = transaction.get("operationAmount", {})
        if not operation_amount:
            raise ValueError("operationAmount не найден в транзакции")

        amount_str = operation_amount.get("amount")
        currency_data = operation_amount.get("currency", {})
        currency_code = currency_data.get("code")

        if amount_str is None:
            raise ValueError("Сумма операции не найдена")

        if currency_code is None:
            raise ValueError("Код валюты не найден")

        amount = float(amount_str)

        if currency_code == "RUB":
            return amount

        if currency_code in ["USD", "EUR"]:
            try:
                exchange_rate = get_exchange_rate(currency_code, "RUB")
                return amount * exchange_rate
            except Exception as e:
                raise Exception(f"Ошибка конвертации валюты {currency_code}: {str(e)}")

        return amount

    except ValueError as e:
        if "не найдена" in str(e) or "не найден" in str(e):
            raise
        raise ValueError(f"Неверный форма суммы: {str(e)}")
    except TypeError as e:
        raise ValueError(f"Неверный тип данных : {str(e)}")
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле : {str(e)}")
