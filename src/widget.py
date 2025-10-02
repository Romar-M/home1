
from src.masks import get_mask_card_number
from src.masks import get_mask_account

def mask_account_card(account_or_card: str) -> str:
    """" Функция, маскирующая счет либо номер карты, в зависимости от ввода данных"""
    parts = account_or_card.split()
    type_str = parts[0] # наименование ввода счет\карта
    number = ' '.join(parts[1:]) # остаток ввода в виде цифр(str)
    if "Счет" in type_str:
        mask_number = get_mask_account(number)
        return f"{type_str} {mask_number}" # выход функции счет
    else:
        mask_number = get_mask_card_number(number)
        return f"{type_str} {mask_number}" # выход функции номер карты

account_or_card = input() # входной аргумент
title: str
print(mask_account_card(account_or_card))


def get_date(date_and_time: str) -> str:
    data_or_time = date_and_time.split('T')  # Разделяем дату и время
    date = data_or_time[0]  # Отделение даты
    day = date[8:10]
    month = date[5:7]
    year = date[0:4]
    return f"{"ДД.ММ.ГГГГ"} {day}.{month}.{year}"

date_and_time = input() # входной аргумент
title: str
print(get_date(date_and_time))
