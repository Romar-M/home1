from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.data_loader import load_transactions_from_csv, load_transactions_from_excel

if __name__ == "__main__":
    # Ввод и вывод для маскировки карты
    card_number = input("Введите номер карты: ")
    masked_card = get_mask_card_number(card_number)
    print(masked_card)

    # Ввод и вывод для маскировки счета
    account_number = input("Введите номер счета: ")
    masked_account = get_mask_account(account_number)
    print(masked_account)

    # Ввод и вывод для умной маскировки
    account_or_card = input("Введите данные карты или счета: ")
    smart_masked = mask_account_card(account_or_card)
    print(smart_masked)

    # Ввод и вывод для форматирования даты
    date_input = input("Введите дату: ")
    formatted_date = get_date(date_input)
    print(formatted_date)

    # Ввод и вывод для фильтрации операций
    state = input("Введите статус операций: ")
    operations_list = []
    filtered_operations = filter_by_state(operations_list, state)
    print(filtered_operations)

    # Ввод и вывод для сортировки операций
    reverse_input = input("Сортировать по убыванию (true/false): ")
    reverse_sort = reverse_input.lower() == "true"
    sorted_operations = sort_by_date(operations_list, reverse_sort)
    print(sorted_operations)
