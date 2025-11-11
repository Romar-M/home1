import pytest
from src.widget import mask_account_card, get_date


class TestWidget:
    """Тесты для модуля widget"""

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Счет 1234567890123456", "Счет **3456"),
    ])
    def test_mask_account_card_valid(self, input_data, expected):
        """Тестирование правильности маскирования карт и счетов"""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("invalid_input", [
        "Visa 123",                    # неверный номер карты
        "Счет 123",                    # неверный номер счета
        "Visa abcdefghijklmnop",       # буквы в номере карты
        "Счет abc",                    # буквы в номере счета
        "",                            # пустая строка
        "Visa",                        # только тип
        "1234567890",                  # только номер
        None,                          # None вместо строки
        12345,                         # число вместо строки
        ["Visa", "1234567890123456"],  # список вместо строки
    ])
    def test_mask_account_card_invalid_input(self, invalid_input):
        """Тестирование функции с некорректными входными данными"""
        assert mask_account_card(invalid_input) == "Неверный формат данных"

    @pytest.mark.parametrize("date_input, expected", [
        ("2024-03-14T10:30:00", "14.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2020-01-01T00:00:00", "01.01.2020"),
    ])
    def test_get_date_valid(self, date_input, expected):
        """Тестирование правильности преобразования даты"""
        assert get_date(date_input) == expected

    @pytest.mark.parametrize("invalid_date", [
        "2024-03-14",                    # без времени
        "2024/03/14T10:30:00",           # неправильный разделитель
        "14.03.2024",                    # уже в нужном формате
        "",                              # пустая строка
        "T10:30:00",                     # только время
        "2024-03-14T",                   # неполная дата
        "2024-03-14T10:30",              # неполное время
        "2024-03-14T10:30:00.000",       # с миллисекундами
        "2024-03-14T10:30:00Z",          # с временной зоной
        "2024-13-14T10:30:00",           # неверный месяц
        "2024-03-32T10:30:00",           # неверный день
        "abcd-ef-ghT10:30:00",           # буквы вместо цифр
        "2024-03-14T10:30:00extra",      # лишние символы
        "2024-03-14T25:30:00",           # неверный час
        None,                            # None вместо строки
        20240314,                        # число вместо строки
        ["2024", "03", "14"],            # список вместо строки
    ])
    def test_get_date_invalid_format(self, invalid_date):
        """Тестирование функции с нестандартными форматами дат"""
        assert get_date(invalid_date) == "Неверный формат данных"
