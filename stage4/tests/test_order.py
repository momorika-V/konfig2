"""Тесты порядка загрузки зависимостей (этап 4)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import load_order

SIMPLE_GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
CYCLE_GRAPH = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}


class LoadOrderTest(unittest.TestCase):
    """Проверка порядка загрузки: зависимости раньше зависящих."""

    def test_linear_chain(self):
        """Для цепочки A -> B -> C порядок C, B, A."""
        order = load_order({"A": ["B"], "B": ["C"], "C": []}, "A")
        self.assertEqual(order, ["C", "B", "A"])

    def test_diamond(self):
        """Общая зависимость D встречается в списке один раз."""
        order = load_order(SIMPLE_GRAPH, "A")
        self.assertEqual(order.index("D"), 0)
        self.assertLess(order.index("B"), order.index("A"))
        self.assertLess(order.index("C"), order.index("A"))
        self.assertEqual(len([n for n in order if n == "D"]), 1)

    def test_cycle_completes(self):
        """Цикл не приводит к бесконечному обходу."""
        order = load_order(CYCLE_GRAPH, "A")
        self.assertEqual(sorted(order), ["A", "B", "C", "D"])
        self.assertEqual(order[-1], "A")


if __name__ == "__main__":
    unittest.main()
