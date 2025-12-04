import datetime
from functools import wraps


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем текущее время
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Выполнение функции
                result = func(*args, **kwargs)

                log_message = f"{current_time} {func_name} ok\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{current_time} {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                raise

        return wrapper

    return decorator
