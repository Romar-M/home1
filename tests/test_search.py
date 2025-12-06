from src.search import process_bank_search, process_bank_operations


class TestSearchFunctions:
    """Тесты для функций поиска и обработки банковских операций"""

    def test_process_bank_search_basic(self):
        """Базовый тест поиска операций"""
        data = [
            {"description": "Перевод организации", "amount": 100},
            {"description": "Оплата услуг", "amount": 200},
            {"description": "Перевод другу", "amount": 300},
        ]

        result = process_bank_search(data, "Перевод")
        assert len(result) == 2
        assert result[0]["description"] == "Перевод организации"
        assert result[1]["description"] == "Перевод другу"

    def test_process_bank_search_case_insensitive(self):
        """Тест регистронезависимого поиска"""
        data = [
            {"description": "Перевод организации", "amount": 100},
            {"description": "перевод другу", "amount": 200},
            {"description": "ПЕРЕВОД самому себе", "amount": 300},
        ]

        result = process_bank_search(data, "перевод")
        assert len(result) == 3

    def test_process_bank_search_empty(self):
        """Тест поиска с пустыми данными"""
        assert process_bank_search([], "Перевод") == []
        assert process_bank_search([{"description": "Тест"}], "") == []

    def test_process_bank_operations_basic(self):
        """Базовый тест подсчета операций по категориям"""
        data = [
            {"description": "Перевод организации"},
            {"description": "Перевод другу"},
            {"description": "Оплата услуг"},
            {"description": "Открытие вклада"},
            {"description": "Перевод организации"},
        ]

        categories = ["Перевод", "Оплата", "Открытие"]
        result = process_bank_operations(data, categories)

        assert result["Перевод"] == 3
        assert result["Оплата"] == 1
        assert result["Открытие"] == 1

    def test_process_bank_operations_case_insensitive(self):
        """Тест регистронезависимого подсчета"""
        data = [
            {"description": "перевод организации"},
            {"description": "Перевод другу"},
            {"description": "ПЕРЕВОД самому себе"},
        ]

        categories = ["перевод", "ПЕРЕВОД"]
        result = process_bank_operations(data, categories)

        assert result["перевод"] == 3
        assert result["ПЕРЕВОД"] == 3

    def test_process_bank_operations_empty(self):
        """Тест подсчета с пустыми данными"""
        assert process_bank_operations([], ["Перевод"]) == {"Перевод": 0}
        assert process_bank_operations([{"description": "Тест"}], []) == {}

    def test_process_bank_search_special_characters(self):
        """Тест поиска с специальными символами"""
        data = [
            {"description": "Оплата (срочная)"},
            {"description": "Перевод 100$"},
            {"description": "Оплата-предоплата"},
        ]

        result = process_bank_search(data, "Оплата")
        assert len(result) == 2

        result = process_bank_search(data, "100$")
        assert len(result) == 1
