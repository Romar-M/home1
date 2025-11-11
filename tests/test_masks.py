import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestMasks:
    """Тесты для модуля masks"""

    @pytest.mark.parametrize("card_number, expected", [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тестирование правильности маскирования номера карты"""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("card_number", [
        "123456789012345",      # 15 цифр
        "12345678901234567",    # 17 цифр
        "12345678901234",       # 14 цифр
        "1234567890123abc",     # буквы в номере
        "",                     # пустая строка
        "1234",                 # слишком короткий номер
        None,                   # None вместо строки
        1234567890123456,       # число вместо строки
    ])
    def test_get_mask_card_number_invalid(self, card_number):
        """Тестирование работы функции на некорректных номерах карт"""
        assert get_mask_card_number(card_number) is None

    @pytest.mark.parametrize("account_number, expected", [
        ("12345678901234567890", "**7890"),
        ("1234567890123456", "**3456"),
        ("1234567890", "**7890"),
    ])
    def test_get_mask_account_valid(self, account_number, expected):
        """Тестирование правильности маскирования номера счета"""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize("account_number", [
        "123",                  # 3 цифры
        "12",                   # 2 цифры
        "1",                    # 1 цифра
        "",                     # пустая строка
        "abc",                  # буквы
        "123abc",               # буквы и цифры
        None,                   # None вместо строки
        1234567890,             # число вместо строки
    ])
    def test_get_mask_account_invalid(self, account_number):
        """Тестирование функции с некорректными номерами счетов"""
        assert get_mask_account(account_number) is None
