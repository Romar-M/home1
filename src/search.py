import re
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует банковские операции по строке поиска в описании.
    """
    if not data or not search:
        return []

    filtered_data = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        description = operation.get('description', '')
        if description and pattern.search(description):
            filtered_data.append(operation)

    return filtered_data


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.
    """
    result = {category: 0 for category in categories}

    if not data or not categories:
        return result

    for operation in data:
        description = operation.get('description', '')
        if description:
            # Приводим описание к нижнему регистру для сравнения
            desc_lower = description.lower()
            for category in categories:
                if category.lower() in desc_lower:
                    result[category] += 1

    return result
