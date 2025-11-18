def filter_by_currency(transactions, currency):
    """Функция, принимает список транзакций, возвращает транзакции по определенной валюте"""

    for transaction in transactions:
        # Проверяем наличие необходимых ключей
        if (
            isinstance(transaction, dict)
            and "operationAmount" in transaction
            and isinstance(transaction["operationAmount"], dict)
            and "currency" in transaction["operationAmount"]
            and isinstance(transaction["operationAmount"]["currency"], dict)
            and "code" in transaction["operationAmount"]["currency"]
        ):

            # Сравниваем код валюты транзакции с заданной валютой
            if transaction["operationAmount"]["currency"]["code"] == currency:
                yield transaction


def transaction_descriptions(transactions: list):
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди.
    """

    for transaction in transactions:
        # Проверяем, что транзакция является словарем и содержит ключ 'description'
        if isinstance(transaction, dict) and "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, end: int):
    """
    Генератор номеров банковских карт.

    """
    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями
        card_str = str(number).zfill(16)

        # Форматируем в виде XXXX XXXX XXXX XXXX
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card
