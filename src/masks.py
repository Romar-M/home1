def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]  # выход функции


card_number = input()  # входной аргумент
print(get_mask_card_number(card_number))


def get_mask_account(account_number: str) -> str:
    """Функция маскировки банковского счета"""
    return "**" + account_number[-4:]  # выход функции


account_number = input()  # входной аргумент
title: str
print(get_mask_account(account_number))
