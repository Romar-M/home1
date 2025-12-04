from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestFilterByCurrency:

    def test_filter_usd_currency(self):
        transactions = [
            {"id": 1, "operationAmount": {"amount": "1000", "currency": {"code": "USD"}}},
            {"id": 2, "operationAmount": {"amount": "500", "currency": {"code": "RUB"}}},
        ]

        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_empty_transactions_list(self):
        result = list(filter_by_currency([], "USD"))
        assert len(result) == 0

    def test_no_matching_currency(self):
        transactions = [{"id": 1, "operationAmount": {"amount": "1000", "currency": {"code": "EUR"}}}]

        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 0

    def test_missing_operation_amount(self):
        transactions = [
            {"id": 1},  # нет operationAmount
            {"id": 2, "operationAmount": {"amount": "1000"}},  # нет currency
        ]

        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 0


class TestTransactionDescriptions:

    def test_get_descriptions(self):
        transactions = [{"id": 1, "description": "Перевод организации"}, {"id": 2, "description": "Оплата услуг"}]

        result = list(transaction_descriptions(transactions))
        assert result == ["Перевод организации", "Оплата услуг"]

    def test_empty_transactions_list(self):

        result = list(transaction_descriptions([]))
        assert result == []

    def test_missing_description_field(self):
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "state": "EXECUTED"},  # нет description
            {"id": 3, "description": "Оплата услуг"},
        ]

        result = list(transaction_descriptions(transactions))
        assert result == ["Перевод организации", "Оплата услуг"]

    def test_invalid_transaction_types(self):
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            "invalid_string",  # не словарь
            {"id": 3, "description": "Оплата услуг"},
        ]

        result = list(transaction_descriptions(transactions))
        assert result == ["Перевод организации", "Оплата услуг"]


class TestCardNumberGenerator:

    def test_small_range(self):
        """Тестирование малого диапазона"""
        result = list(card_number_generator(1, 3))
        expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
        assert result == expected

    def test_single_number(self):
        result = list(card_number_generator(1, 1))
        assert result == ["0000 0000 0000 0001"]

    def test_large_numbers(self):
        result = list(card_number_generator(9999999999999998, 9999999999999999))
        expected = ["9999 9999 9999 9998", "9999 9999 9999 9999"]
        assert result == expected

    def test_format_correctness(self):

        result = next(card_number_generator(1234567812345678, 1234567812345678))

        # Проверяем формат
        assert len(result) == 19  # 16 цифр + 3 пробела
        parts = result.split(" ")
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)
        assert result == "1234 5678 1234 5678"
