# Список словарей
list_of_dictionaries = []


def filter_by_state(operations: list, state: str) -> list:
    """Возвращает список словарей по значению ключа 'state'"""

    output_list = []

    for operation in operations:
      if operation.get('state') == state:
          output_list.append(operation)
    return output_list


state = input() or 'EXECUTED'
title: str

print(filter_by_state(list_of_dictionaries, state))


def sort_by_date(list, reverse=True):
    """Фильтрует список словарей по дате"""

    return sorted(list, key=lambda x: x['date'], reverse=reverse)


print(sort_by_date(list_of_dictionaries, True))

print(sort_by_date(list_of_dictionaries, False))