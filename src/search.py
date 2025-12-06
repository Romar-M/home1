import re
from collections import Counter
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
    if not data or not categories:
        return {category: 0 for category in categories}

    counter = Counter()

    for operation in data:
        description = operation.get('description', '')
        if description:
            desc_lower = description.lower()
            for category in categories:
                if category.lower() in desc_lower:
                    counter[category] += 1

    return dict(counter)
