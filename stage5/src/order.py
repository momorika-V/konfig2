"""Определение порядка загрузки зависимостей графа.

Порядок строится обходом DFS без рекурсии: пакет добавляется в список
после того, как обработаны все его зависимости (обратный порядок
завершения вершин). Поэтому каждая зависимость встречается в списке
раньше зависящего от неё пакета.
"""


def load_order(graph, start):
    """Возвращает пакеты в порядке загрузки (зависимости — раньше).

    Для циклических зависимостей строгий порядок не существует; в этом
    случае пакеты цикла выводятся в порядке обхода, что отражено в
    README (сравнение с реальным менеджером пакетов).
    """
    order = []
    visited = set()
    stack = [(start, False)]
    while stack:
        name, expanded = stack.pop()
        if expanded:
            order.append(name)
            continue
        if name in visited:
            continue
        visited.add(name)
        stack.append((name, True))
        for dep in graph.get(name, []):
            if dep not in visited:
                stack.append((dep, False))
    return order


def print_order(order):
    """Печатает порядок загрузки с номерами шагов."""
    print("Порядок загрузки:")
    for step, name in enumerate(order, start=1):
        print(f"  {step}. {name}")
