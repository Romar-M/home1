import pytest
from collections import Counter
from src.search import process_bank_search, process_bank_operations


class TestFixedSearchFunctions:
    """Тесты для исправленных функций поиска"""

    def test_process_bank_search_with_re(self):
        """Тест поиска с использованием регулярных выражений"""
        data = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Оплата услуг ЖКХ"},
            {"id": 3, "description": "Перевод другу"},
            {"id": 4, "description": "Перевод организации (срочный)"},
        ]

        # Поиск подстроки в любой части описания
        result = process_bank_search(data, "Перевод")
        assert len(result) == 3
        assert all("Перевод" in op["description"] for op in result)

        # Регистронезависимый поиск
        result = process_bank_search(data, "перевод")
        assert len(result) == 3

    def test_process_bank_operations_with_counter(self):
        """Тест подсчета операций с использованием Counter"""
        data = [
            {"description": "Перевод организации"},
            {"description": "Перевод другу"},
            {"description": "Оплата услуг"},
            {"description": "Открытие вклада"},
            {"description": "Перевод организации"},
            {"description": "Пополнение счета"},
        ]

        categories = ["Перевод", "Оплата", "Открытие", "Пополнение"]
        result = process_bank_operations(data, categories)

        assert result["Перевод"] == 3
        assert result["Оплата"] == 1
        assert result["Открытие"] == 1
        assert result["Пополнение"] == 1

        assert isinstance(result, dict)
        assert not isinstance(result, Counter)

    def test_process_bank_operations_empty_data(self):
        """Тест с пустыми данными"""
        result = process_bank_operations([], ["Перевод", "Оплата"])
        assert result == {"Перевод": 0, "Оплата": 0}

        result = process_bank_operations([{"description": "Тест"}], [])
        assert result == {}

    def test_search_special_characters(self):
        """Тест поиска с специальными символами"""
        data = [
            {"description": "Оплата (срочная)"},
            {"description": "Перевод 100$ на счет"},
            {"description": "Оплата-предоплата за услуги"},
        ]

        result = process_bank_search(data, "100$")
        assert len(result) == 1
        assert result[0]["description"] == "Перевод 100$ на счет"

        result = process_bank_search(data, "(срочная)")
        assert len(result) == 1
