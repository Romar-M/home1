import pytest
import os
import requests
from unittest.mock import patch, Mock
from src.external_api import get_amount_in_rub, get_exchange_rate


class TestExternalAPI:
    """Тесты для функций работы с внешним API"""

    def test_get_amount_in_rub_rub(self):
        """Тестирование получения суммы в рублях для RUB транзакции"""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"}
            }
        }

        result = get_amount_in_rub(transaction)
        assert result == 1000.50
        assert isinstance(result, float)

    @patch('src.external_api.get_exchange_rate')
    def test_get_amount_in_rub_usd(self, mock_get_rate):
        """Тестирование конвертации USD в RUB"""
        mock_get_rate.return_value = 75.5

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"}
            }
        }

        result = get_amount_in_rub(transaction)
        assert result == 7550.0  # 100 * 75.5
        mock_get_rate.assert_called_once_with('USD', 'RUB')

    @patch('src.external_api.get_exchange_rate')
    def test_get_amount_in_rub_eur(self, mock_get_rate):
        """Тестирование конвертации EUR в RUB"""
        mock_get_rate.return_value = 85.3

        transaction = {
            "operationAmount": {
                "amount": "50.0",
                "currency": {"code": "EUR"}
            }
        }

        result = get_amount_in_rub(transaction)
        assert result == 4265.0  # 50 * 85.3
        mock_get_rate.assert_called_once_with('EUR', 'RUB')

    def test_get_amount_in_rub_invalid_transaction(self):
        """Тестирование с невалидной транзакцией"""
        with pytest.raises(ValueError, match="Транзакция должна быть словарем"):
            get_amount_in_rub("invalid_transaction")

    def test_get_amount_in_rub_missing_operation_amount(self):
        """Тестирование с транзакцией без operationAmount"""
        transaction = {"id": 1}

        with pytest.raises(ValueError, match="operationAmount не найден в транзакции"):
            get_amount_in_rub(transaction)

    def test_get_amount_in_rub_missing_amount(self):
        """Тестирование с транзакцией без суммы"""
        transaction = {
            "operationAmount": {
                "currency": {"code": "RUB"}
            }
        }

        with pytest.raises(ValueError, match="Сумма операции не найдена"):
            get_amount_in_rub(transaction)

    def test_get_amount_in_rub_missing_currency_code(self):
        """Тестирование с транзакцией без кода валюты"""
        transaction = {
            "operationAmount": {
                "amount": "1000.0",
                "currency": {}
            }
        }

        with pytest.raises(ValueError, match="Код валюты не найден"):
            get_amount_in_rub(transaction)

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тестирование успешного получения курса валют"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'rates': {'RUB': 75.5}
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            rate = get_exchange_rate('USD', 'RUB')

        assert rate == 75.5
        mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_api_error(self, mock_get):
        """Тестирование ошибки API"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            with pytest.raises(Exception, match="Ошибка API запроса"):
                get_exchange_rate('USD', 'RUB')

    def test_get_exchange_rate_no_api_key(self):
        """Тестирование отсутствия API ключа"""
        if 'EXCHANGE_RATE_API_KEY' in os.environ:
            del os.environ['EXCHANGE_RATE_API_KEY']

        with pytest.raises(ValueError, match="API ключ не найден"):
            get_exchange_rate('USD', 'RUB')

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_timeout(self, mock_get):
        """Тестирование таймаута при запросе"""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            with pytest.raises(Exception, match="Таймаут при запросе к API"):
                get_exchange_rate('USD', 'RUB')
