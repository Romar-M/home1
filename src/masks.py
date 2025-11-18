def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    if not card_number or not isinstance(card_number, str) or len(card_number) != 16 or not card_number.isdigit():
        return None
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """Функция маскировки банковского счета"""
    if (
        not account_number
        or not isinstance(account_number, str)
        or len(account_number) < 4
        or not account_number.isdigit()
    ):
        return None
    return "**" + account_number[-4:]
