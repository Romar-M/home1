# импорт функций маскировки
from src.masks import get_mask_card_number
from src.masks import get_mask_account


def mask_account_card(account_or_card: str) -> str:
    """Функция, маскирующая счет либо номер карты, в зависимости от ввода данных"""

    parts = account_or_card.split()  # Определяем тип карты/счета
    type_str = " ".join(parts[:-1])
    number = parts[-1]  # Номер (последний элемент)

    if "Счет" in type_str:
        mask_number = get_mask_account(number)
        return f"{type_str} {mask_number}"
    else:
        mask_number = get_mask_card_number(number)
        return f"{type_str} {mask_number}"  # выход функции номер карты


account_or_card = input()  # входной аргумент
title: str
print(mask_account_card(account_or_card))


def get_date(date_and_time: str) -> str:
    """Функция, переводящая введенную дата и время в формат дд.мм.гггг"""
    data_or_time = date_and_time.split("T")  # Разделяем дату и время
    date = data_or_time[0]  # Отделение даты
    day = date[8:10]
    month = date[5:7]
    year = date[0:4]
    return f"{day}.{month}.{year}"


date_and_time = input()  # входной аргумент
title: str
print(get_date(date_and_time))
