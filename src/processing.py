list_of_dictionaries = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
      ]


def filter_by_state(dicts: list, state: str) -> list:
    """
    Фильтрует список словарей по значению ключа 'state'
    """
    output_list = []
    for i in dicts:
      if i.get('state') == state:
          output_list.append(i)
    return output_list






state = input() or 'EXECUTED'
title: str

print(filter_by_state(list_of_dictionaries, state))







#
# def sort_by_date(список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание)
#
# return новый список, отсортированный по дате
