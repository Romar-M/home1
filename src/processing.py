# Список словарей
operations_list = []


def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """Возвращает список словарей по значению ключа 'state'"""
    filtered_list = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_list.append(operation)
    return filtered_list


user_state = input() or "EXECUTED"
print(filter_by_state(operations_list, user_state))


def sort_by_date(operations: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате"""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)


print(sort_by_date(operations_list, True))
print(sort_by_date(operations_list, False)
