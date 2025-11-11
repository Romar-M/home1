def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """Возвращает список словарей по значению ключа 'state'"""
    if not operations or not isinstance(operations, list):
        return []

    filtered_list = []
    for operation in operations:
        if isinstance(operation, dict) and operation.get("state") == state:
            filtered_list.append(operation)
    return filtered_list


def sort_by_date(operations: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате"""
    if not operations or not isinstance(operations, list):
        return []

    try:
        return sorted(operations, key=lambda x: x["date"], reverse=reverse)
    except (KeyError, TypeError):
        return []
