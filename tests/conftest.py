import pytest


@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми данными операций"""
    return [
        {
            "state": "EXECUTED",
            "date": "2024-03-14T10:30:00",
            "id": 1,
            "description": "Перевод организации",
            "amount": 1000,
        },
        {"state": "PENDING", "date": "2024-03-13T15:45:00", "id": 2, "description": "Перевод другу", "amount": 500},
        {"state": "EXECUTED", "date": "2024-03-12T09:15:00", "id": 3, "description": "Оплата услуг", "amount": 1500},
        {"state": "CANCELED", "date": "2024-03-11T14:20:00", "id": 4, "description": "Отмена заказа", "amount": 2000},
        {
            "state": "EXECUTED",
            "date": "2024-03-10T08:00:00",
            "id": 5,
            "description": "Пополнение счета",
            "amount": 3000,
        },
    ]


@pytest.fixture
def operations_with_same_date():
    """Фикстура с операциями с одинаковыми датами"""
    return [
        {"state": "EXECUTED", "date": "2024-03-14T10:30:00", "id": 1},
        {"state": "EXECUTED", "date": "2024-03-14T10:30:00", "id": 2},
        {"state": "PENDING", "date": "2024-03-14T10:30:00", "id": 3},
    ]


@pytest.fixture
def complex_operations_fixture():
    """Комплексная фикстура с различными случаями для тестирования"""
    return [
        {"state": "EXECUTED", "date": "2024-01-15T12:00:00", "amount": 100},
        {"state": "PENDING", "date": "2024-01-14T11:30:00", "amount": 200},
        {"state": "EXECUTED", "date": "2024-01-13T10:15:00", "amount": 150},
        {"state": "CANCELED", "date": "2024-01-12T09:45:00", "amount": 300},
        {"state": "EXECUTED", "date": "2024-01-11T08:30:00", "amount": 250},
    ]
