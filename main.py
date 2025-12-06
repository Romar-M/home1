from typing import List, Dict, Any
from src.utils import load_operations
from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.external_api import get_amount_in_rub
from src.widget import mask_account_card, get_date
from src.search import process_bank_search, process_bank_operations


def get_valid_status() -> str:
    """Запрашивает у пользователя валидный статус операции"""
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию.\n"
                       f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}\n"
                       "Ваш выбор: ").strip().upper()

        if status in valid_statuses:
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def get_user_choice(prompt: str, valid_options: List[str]) -> str:
    """Запрашивает у пользователя выбор из допустимых вариантов"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print(f"Пожалуйста, выберите один из вариантов: {', '.join(valid_options)}")


def print_operation(operation: dict) -> None:
    """Выводит информацию об одной операции в консоль"""
    date = get_date(operation.get('date', '')) if operation.get('date') else 'Дата не указана'

    description = operation.get('description', 'Без описания')

    from_account = mask_account_card(operation.get('from', 'N/A'))
    to_account = mask_account_card(operation.get('to', 'N/A'))

    amount_rub = 0
    try:
        amount_rub = get_amount_in_rub(operation)
    except Exception:
        pass

    print(f"\n{date} {description}")
    if operation.get('from'):
        print(f"{from_account} -> {to_account}")
    else:
        print(f"{to_account}")
    print(f"Сумма: {amount_rub:.2f} руб.")


def main() -> None:
    """Основная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input("Ваш выбор: ").strip()

    operations = []
    file_path = ""

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = "data/operations.json"
        operations = load_operations(file_path)
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = "data/transactions.csv"
        operations = load_transactions_from_csv(file_path)
    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = "data/transactions_excel.xlsx"
        operations = load_transactions_from_excel(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not operations:
        print(f"Не удалось загрузить операции из файла {file_path}")
        return

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_operations = filter_by_state(operations, status)
    print(f"Операции отфильтрованы по статусу '{status}'")

    if not filtered_operations:
        print("Не найдено операций с выбранным статусом.")
        return

    # Сортировка по дате
    sort_choice = get_user_choice("Отсортировать операции по дате? (да/нет): ", ['да', 'нет'])

    if sort_choice == 'да':
        order_choice = get_user_choice("Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ",
                                       ['по возрастанию', 'по убыванию'])

        reverse = True if order_choice == 'по убыванию' else False
        filtered_operations = sort_by_date(filtered_operations, reverse)

    # Фильтрация по валюте
    currency_choice = get_user_choice("Выводить только рублевые транзакции? (да/нет): ", ['да', 'нет'])

    if currency_choice == 'да':
        rub_operations = []
        for op in filtered_operations:
            try:
                amount_rub = get_amount_in_rub(op)
                rub_operations.append(op)
            except Exception:
                continue

        filtered_operations = rub_operations

    # Поиск по ключевому слову
    search_choice = get_user_choice("Отфильтровать список транзакций по определенному слову в описании? (да/нет): ",
                                    ['да', 'нет'])

    if search_choice == 'да':
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_operations = process_bank_search(filtered_operations, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_operations)}\n")

    if not filtered_operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    for operation in filtered_operations:
        print_operation(operation)

    # Дополнительная статистика
    print("\n" + "=" * 50)
    print("Статистика по категориям операций:")

    categories = ['Перевод', 'Открытие вклада', 'Оплата услуг', 'Пополнение счета']
    category_stats = process_bank_operations(filtered_operations, categories)

    for category, count in category_stats.items():
        if count > 0:
            print(f"{category}: {count} операций")


if __name__ == "__main__":
    main()
