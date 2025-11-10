def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


card_number = input()
print(get_mask_card_number(card_number))


def get_mask_account(account_number: str) -> str:
    """Функция маскировки банковского счета"""
    return "**" + account_number[-4:]


account_number = input()
print(get_mask_account(account_number))
