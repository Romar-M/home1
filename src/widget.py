from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(account_or_card: str) -> str:
    """Функция, маскирующая счет либо номер карты, в зависимости от ввода данных"""
    if not account_or_card or not isinstance(account_or_card, str):
        return "Неверный формат данных"

    parts = account_or_card.split()
    if len(parts) < 2:
        return "Неверный формат данных"

    account_type = " ".join(parts[:-1])
    number = parts[-1]

    if "Счет" in account_type:
        masked_number = get_mask_account(number)
        if masked_number is None:
            return "Неверный формат данных"
        return f"{account_type} {masked_number}"
    else:
        masked_number = get_mask_card_number(number)
        if masked_number is None:
            return "Неверный формат данных"
        return f"{account_type} {masked_number}"


def get_date(date_and_time: str) -> str:
    """Функция, переводящая введенную дату и время в формат дд.мм.гггг"""
    # Простая проверка: строка должна быть длиной 19 символов и содержать T
    if (not date_and_time or not isinstance(date_and_time, str) or
            len(date_and_time) != 19 or "T" not in date_and_time):
        return "Неверный формат данных"

    try:
        # Простое разделение на дату и время
        date_part, time_part = date_and_time.split("T")

        # Проверяем базовый формат даты и времени
        if (len(date_part) != 10 or date_part[4] != '-' or date_part[7] != '-' or
                len(time_part) != 8 or time_part[2] != ':' or time_part[5] != ':'):
            return "Неверный формат данных"

        # Извлекаем компоненты даты
        year = date_part[:4]
        month = date_part[5:7]
        day = date_part[8:10]

        # Проверяем, что все части - цифры
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return "Неверный формат данных"

        # Преобразуем в числа для проверки диапазонов
        year_num = int(year)
        month_num = int(month)
        day_num = int(day)

        # Простые проверки диапазонов
        if not (1 <= month_num <= 12 and 1 <= day_num <= 31 and 1900 <= year_num <= 2100):
            return "Неверный формат данных"

        # Возвращаем дату в нужном формате
        return f"{day}.{month}.{year}"

    except (ValueError, IndexError):
        return "Неверный формат данных"
