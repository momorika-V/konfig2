"""Тесты построения графа зависимостей (этап 3)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import (
    TestRepoLoader, build_graph, is_excluded, load_test_graph)

SIMPLE_REPO = "A: B, C\nB: D\nC: D\nD:\n"
CYCLE_REPO = "A: B\nB: C\nC: A, D\nD:\n"
FILTER_REPO = "A: baX, bb\nbaX:\nbb:\n"


class GraphTestCase(unittest.TestCase):
    """Базовый класс с помощником создания тестовых файлов."""

    def make_repo_file(self, text):

        """Создаёт временный файл тестового репозитория."""

        handle = tempfile.NamedTemporaryFile(

            mode="w", suffix=".txt", delete=False, encoding="utf-8")

        handle.write(text)

        handle.close()

        self.addCleanup(os.unlink, handle.name)

        return handle.name


class LoadTestGraphTest(GraphTestCase):
    """Чтение файла описания тестового репозитория."""

    def test_simple_graph(self):
        """Строки файла превращаются в словарь зависимостей."""
        graph = load_test_graph(self.make_repo_file(SIMPLE_REPO))
        self.assertEqual(
            graph, {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []})

    def test_comments_and_blanks(self):
        """Пустые строки и комментарии игнорируются."""
        text = "# комментарий\n\nA:\n"
        graph = load_test_graph(self.make_repo_file(text))
        self.assertEqual(graph, {"A": []})


class BuildGraphTest(GraphTestCase):
    """Построение графа алгоритмом DFS без рекурсии."""

    def test_transitive_deps(self):
        """В граф попадают транзитивные зависимости."""
        loader = TestRepoLoader(self.make_repo_file(SIMPLE_REPO))
        graph = build_graph("A", loader, "")
        self.assertEqual(set(graph), {"A", "B", "C", "D"})

    def test_cycle(self):
        """Циклические зависимости не приводят к зацикливанию."""
        loader = TestRepoLoader(self.make_repo_file(CYCLE_REPO))
        graph = build_graph("A", loader, "")
        self.assertEqual(set(graph), {"A", "B", "C", "D"})
        self.assertEqual(graph["C"], ["A", "D"])

    def test_filter_excludes_names(self):
        """Пакеты с подстрокой фильтра исключаются из анализа."""
        loader = TestRepoLoader(self.make_repo_file(FILTER_REPO))
        graph = build_graph("A", loader, "baX")
        self.assertNotIn("baX", graph)
        self.assertIn("bb", graph)


class IsExcludedTest(unittest.TestCase):
    """Проверка фильтрации по подстроке."""

    def test_empty_filter_keeps_all(self):
        """Пустой фильтр ничего не исключает."""
        self.assertFalse(is_excluded("anything", ""))

    def test_substring_match(self):
        """Подстрока внутри имени пакета даёт исключение."""
        self.assertTrue(is_excluded("libc-musl", "musl"))


if __name__ == "__main__":
    unittest.main()
