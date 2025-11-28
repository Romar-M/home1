import pytest
import json
import tempfile
import os
from src.utils import load_operations


class TestLoadOperations:
    """Тесты для функции load_operations"""

    def test_load_valid_operations(self):
        """Тестирование загрузки валидного JSON файла"""
        test_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {"name": "руб.", "code": "RUB"}
                }
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            result = load_operations(temp_file)
            assert result == test_data
        finally:
            os.unlink(temp_file)

    def test_load_empty_file(self):
        """Тестирование загрузки пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            result = load_operations(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_load_nonexistent_file(self):
        """Тестирование загрузки несуществующего файла"""
        result = load_operations("nonexistent_file.json")
        assert result == []

    def test_load_invalid_json(self):
        """Тестирование загрузки файла с невалидным JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name

        try:
            result = load_operations(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_load_not_list(self):
        """Тестирование загрузки JSON, который не является списком"""
        test_data = {"id": 1, "name": "test"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            result = load_operations(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_load_real_operations_file(self):
        """Тестирование загрузки реального файла operations.json"""
        result = load_operations("data/operations.json")

        assert isinstance(result, list)

        if result:
            first_item = result[0]
            assert "id" in first_item
            assert "state" in first_item
            assert "date" in first_item
            assert "operationAmount" in first_item
