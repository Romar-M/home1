from unittest.mock import patch, MagicMock
from src.data_loader import load_transactions_from_csv, load_transactions_from_excel


class TestDataLoader:
    """Тесты для модуля загрузки данных из CSV и Excel"""

    @patch("src.data_loader.pd.read_csv")
    def test_load_transactions_from_csv_success(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"id": 1, "amount": "1000"}, {"id": 2, "amount": "2000"}]
        mock_read_csv.return_value = mock_df

        result = load_transactions_from_csv("dummy_path.csv")

        assert result is not None
        assert len(result) == 2
        assert result[0]["id"] == 1
        mock_read_csv.assert_called_once_with("dummy_path.csv", dtype=object, keep_default_na=False)
        mock_df.to_dict.assert_called_once_with("records")

    @patch("src.data_loader.pd.read_csv")
    def test_load_transactions_from_csv_file_not_found(self, mock_read_csv):
        """Обработка ситуации, когда CSV-файл не найден"""
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        result = load_transactions_from_csv("missing.csv")

        assert result is None
        mock_read_csv.assert_called_once()

    @patch("src.data_loader.pd.read_excel")
    def test_load_transactions_from_excel_success(self, mock_read_excel):
        """Успешная загрузка данных из Excel"""
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"id": 3, "amount": "3000"}]
        mock_read_excel.return_value = mock_df

        result = load_transactions_from_excel("dummy_path.xlsx", sheet_name="Операции")

        assert result is not None
        assert len(result) == 1
        mock_read_excel.assert_called_once_with(
            "dummy_path.xlsx", sheet_name="Операции", dtype=object, keep_default_na=False
        )

    @patch("src.data_loader.pd.read_excel")
    def test_load_transactions_from_excel_default_sheet(self, mock_read_excel):
        """Загрузка из Excel с листом по умолчанию (первый лист)"""
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"id": 4}]
        mock_read_excel.return_value = mock_df

        result = load_transactions_from_excel("dummy_path.xlsx")
        mock_read_excel.assert_called_once_with(
            "dummy_path.xlsx", sheet_name=None, dtype=object, keep_default_na=False
        )
        assert result is not None
