import pytest
from src.processing import filter_by_state, sort_by_date


class TestProcessing:
    """Тесты для модуля processing"""

    def test_filter_by_state(self, sample_operations):
        """Тестирование фильтрации по статусу"""
        result = filter_by_state(sample_operations, "EXECUTED")
        assert len(result) == 3
        for operation in result:
            assert operation["state"] == "EXECUTED"

    def test_filter_by_state_pending(self, sample_operations):
        """Тестирование фильтрации по статусу PENDING"""
        result = filter_by_state(sample_operations, "PENDING")
        assert len(result) == 1
        assert result[0]["state"] == "PENDING"

    def test_filter_by_state_default(self, sample_operations):
        """Тестирование фильтрации со статусом по умолчанию"""
        result = filter_by_state(sample_operations)
        assert len(result) == 3
        for operation in result:
            assert operation["state"] == "EXECUTED"

    def test_filter_by_state_empty_list(self):
        """Тестирование фильтрации пустого списка"""
        assert filter_by_state([], "EXECUTED") == []

    def test_filter_by_state_no_matching(self, sample_operations):
        """Тестирование фильтрации когда нет совпадений"""
        result = filter_by_state(sample_operations, "UNKNOWN_STATE")
        assert result == []

    def test_filter_by_state_invalid_input(self):
        """Тестирование фильтрации с некорректными входными данными"""
        assert filter_by_state(None, "EXECUTED") == []
        assert filter_by_state("not_a_list", "EXECUTED") == []
        assert filter_by_state([1, 2, 3], "EXECUTED") == []

    def test_sort_by_date_descending(self, sample_operations):
        """Тестирование сортировки по убыванию даты"""
        result = sort_by_date(sample_operations, reverse=True)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_operations):
        """Тестирование сортировки по возрастанию даты"""
        result = sort_by_date(sample_operations, reverse=False)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates)

    def test_sort_by_date_same_dates(self, operations_with_same_date):
        """Тестирование сортировки при одинаковых датах"""
        result = sort_by_date(operations_with_same_date, reverse=True)
        assert len(result) == 3

    def test_sort_by_date_empty_list(self):
        """Тестирование сортировки пустого списка"""
        assert sort_by_date([], True) == []
        assert sort_by_date([], False) == []

    def test_sort_by_date_single_element(self, complex_operations_fixture):
        """Тестирование сортировки списка с одним элементом"""
        single_operation = [complex_operations_fixture[0]]
        result = sort_by_date(single_operation, True)
        assert result == single_operation

    def test_sort_by_date_invalid_input(self):
        """Тестирование сортировки с некорректными входными данными"""
        assert sort_by_date(None, True) == []
        assert sort_by_date("not_a_list", True) == []
        assert sort_by_date([1, 2, 3], True) == []
