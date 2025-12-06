from typing import List
from src.utils import load_operations
from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.processing import filter_by_state, sort_by_date, count_by_category
from src.external_api import get_amount_in_rub
from src.widget import mask_account_card, get_date
from src.search import process_bank_search


def main() -> None:
    """Основная функция программы"""
    # Приветственное сообщение
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Обработка выбора пользователя
    file_choice = input("Ваш выбор: ").strip()

    operations = []
    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        operations = load_operations("data/operations.json")
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        operations = load_transactions_from_csv("data/transactions.csv")
    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        operations = load_transactions_from_excel("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not operations:
        print("Не удалось загрузить операции из файла.")
        return

    # Фильтрация по статусу с приведением к регистру
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}\n"
            "Ваш выбор: "
        ).strip().upper()

        if status_input in valid_statuses:
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    operations = filter_by_state(operations, status_input)
    print(f"Операции отфильтрованы по статусу '{status_input}'")

    # Сортировка по дате
    sort_answer = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_answer in ["да", "д", "yes", "y"]:
        direction = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = True if "убыванию" in direction else False
        operations = sort_by_date(operations, reverse)

    # Только рублевые транзакции
    rub_answer = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if rub_answer in ["да", "д", "yes", "y"]:
        rub_operations = []
        for op in operations:
            try:
                amount_rub = get_amount_in_rub(op)
                # Проверяем, что это рублевая транзакция
                currency = op.get("operationAmount", {}).get("currency", {}).get("code", "")
                if currency == "RUB":
                    rub_operations.append(op)
            except Exception:
                continue
        operations = rub_operations

    # Поиск по слову в описании
    search_answer = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if search_answer in ["да", "д", "yes", "y"]:
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            operations = process_bank_search(operations, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(operations)}\n")

    for operation in operations:
        # Форматирование даты
        date_str = get_date(operation.get("date", "")) if operation.get("date") else "Дата не указана"

        # Описание
        description = operation.get("description", "Без описания")

        # Счета
        from_account = mask_account_card(operation.get("from", "N/A"))
        to_account = mask_account_card(operation.get("to", "N/A"))

        # Сумма
        try:
            amount = get_amount_in_rub(operation)
        except Exception:
            amount = 0

        print(f"{date_str} {description}")
        if operation.get("from"):
            print(f"{from_account} -> {to_account}")
        else:
            print(f"{to_account}")
        print(f"Сумма: {amount:.2f} руб.\n")

    # Статистика по категориям
    categories = ["Перевод", "Открытие вклада", "Оплата услуг", "Пополнение счета"]
    stats = count_by_category(operations, categories)

    print("=" * 50)
    print("Статистика по категориям операций:")
    for category, count in stats.items():
        if count > 0:
            print(f"{category}: {count} операций")


if __name__ == "__main__":
    main()
