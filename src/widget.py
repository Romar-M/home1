# импорт функций маскировки
from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(account_or_card: str) -> str:
    """Функция, маскирующая счет либо номер карты, в зависимости от ввода данных"""
    parts = account_or_card.split()
    account_type = " ".join(parts[:-1])
    number = parts[-1]

    if "Счет" in account_type:
        masked_number = get_mask_account(number)
        return f"{account_type} {masked_number}"
    else:
        masked_number = get_mask_card_number(number)
        return f"{account_type} {masked_number}"


user_input = input()
print(mask_account_card(user_input))


def get_date(date_and_time: str) -> str:
    """Функция, переводящая введенную дату и время в формат дд.мм.гггг"""
    date_part = date_and_time.split("T")[0]
    year = date_part[:4]
    month = date_part[5:7]
    day = date_part[8:10]
    return f"{day}.{month}.{year}"


date_input = input()
print(get_date(date_input))
