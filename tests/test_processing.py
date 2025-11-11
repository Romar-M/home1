import pytest
from src.processing import filter_by_state, sort_by_date


class TestProcessing:
    """Тесты для модуля processing"""

    @pytest.fixture
    def sample_operations(self):
        """Фикстура с тестовыми данными операций"""
        return [
            {"state": "EXECUTED", "date": "2024-03-14T10:30:00", "id": 1},
            {"state": "PENDING", "date": "2024-03-13T15:45:00", "id": 2},
            {"state": "EXECUTED", "date": "2024-03-12T09:15:00", "id": 3},
            {"state": "CANCELED", "date": "2024-03-11T14:20:00", "id": 4},
            {"state": "EXECUTED", "date": "2024-03-10T08:00:00", "id": 5},
        ]

    def test_filter_by_state_invalid_input(self):
        """Тестирование фильтрации с некорректными входными данными"""
        assert filter_by_state(None, "EXECUTED") == []
        assert filter_by_state("not_a_list", "EXECUTED") == []
        assert filter_by_state([], "EXECUTED") == []
        assert filter_by_state([1, 2, 3], "EXECUTED") == []  # список не словарей

    def test_sort_by_date_invalid_input(self):
        """Тестирование сортировки с некорректными входными данными"""
        assert sort_by_date(None, True) == []
        assert sort_by_date("not_a_list", True) == []
        assert sort_by_date([], True) == []
        assert sort_by_date([1, 2, 3], True) == []  # список не словарей
