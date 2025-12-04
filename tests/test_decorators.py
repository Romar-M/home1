import os
import pytest
from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log"""

    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешного выполнения в консоль"""

        @log()
        def add(a, b):
            return a + b

        result = add(1, 2)

        # Проверяем результат функции
        assert result == 3

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "add ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль"""

        @log()
        def divide(a, b):
            return a / b

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (1, 0), {}" in captured.out

    def test_log_to_file_success(self, tmp_path):
        """Тестирование логирования успешного выполнения в файл"""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def multiply(a, b):
            return a * b

        result = multiply(3, 4)

        # Проверяем результат функции
        assert result == 12

        # Проверяем запись в файл
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "multiply ok" in content

    def test_log_to_file_error(self, tmp_path):
        """Тестирование логирования ошибки в файл"""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def failing_func(x):
            raise ValueError("Test error")

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError):
            failing_func(42)

        # Проверяем запись в файл
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "failing_func error: ValueError" in content
        assert "Inputs: (42,), {}" in content

    def test_log_with_keyword_arguments(self, capsys):
        """Тестирование логирования с ключевыми аргументами"""

        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        # Проверяем результат функции
        assert result == "Hi, Alice!"

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "greet ok" in captured.out

    def test_log_preserves_function_metadata(self):
        """Тестирование сохранения метаданных функции"""

        @log()
        def original_function(x):
            """Тестовая функция"""
            return x

        # Проверяем, что метаданные сохранились
        assert original_function.__name__ == "original_function"
        assert original_function.__doc__ == "Тестовая функция"

    def test_multiple_calls_to_file(self, tmp_path):
        """Тестирование множественных вызовов с записью в файл"""
        log_file = tmp_path / "multi_log.txt"

        @log(filename=str(log_file))
        def counter():
            return 1

        # Вызываем функцию несколько раз
        for _ in range(3):
            counter()

        # Проверяем, что в файле 3 записи
        content = log_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) == 3
        assert all("counter ok" in line for line in lines)

    def test_log_with_complex_arguments(self, capsys):
        """Тестирование логирования со сложными аргументами"""

        @log()
        def complex_func(a, b=10, c=None):
            return a + b + (c if c else 0)

        result = complex_func(5, c=15)

        # Проверяем результат функции
        assert result == 30

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "complex_func ok" in captured.out

    def test_cleanup_test_files(self):
        """Очистка тестовых файлов (опционально)"""
        test_files = ["mylog.txt", "test_log.txt", "multi_log.txt"]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
