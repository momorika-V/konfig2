"""Тесты получения данных из sparse-индекса crates.io."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fetcher import (
    choose_record, index_path, parse_version)


class IndexPathTest(unittest.TestCase):
    """Проверка правил построения пути пакета в индексе."""

    def test_one_letter(self):
        """Имя из одной буквы хранится в каталоге 1."""
        self.assertEqual(index_path("a"), "1/a")

    def test_two_letters(self):
        """Имя из двух букв хранится в каталоге 2."""
        self.assertEqual(index_path("ab"), "2/ab")

    def test_three_letters(self):
        """Имя из трёх букв хранится по первой букве."""
        self.assertEqual(index_path("abc"), "3/a/abc")

    def test_long_name(self):
        """Длинное имя хранится по первым четырём буквам."""
        self.assertEqual(index_path("serde_json"), "se/rd/serde_json")


class VersionTest(unittest.TestCase):
    """Проверка разбора и выбора версий пакета."""

    def test_parse_version(self):
        """Строка версии превращается в кортеж чисел."""
        self.assertEqual(parse_version("1.2.10"), (1, 2, 10))

    def test_parse_version_ordering(self):
        """Кортежи версий сравниваются как числа."""
        self.assertGreater(parse_version("1.10.0"), parse_version("1.9.0"))

    def test_choose_latest(self):
        """latest выбирает самую новую версию."""
        records = [{"vers": "1.0.0"}, {"vers": "0.9.0"},
                   {"vers": "1.1.0"}]
        self.assertEqual(choose_record(records, "latest")["vers"],
                         "1.1.0")

    def test_choose_exact(self):
        """Точная версия выбирается по совпадению строки."""
        records = [{"vers": "1.0.0"}, {"vers": "1.1.0"}]
        self.assertEqual(choose_record(records, "1.0.0")["vers"],
                         "1.0.0")

    def test_choose_missing(self):
        """Незаданная версия даёт пустой результат."""
        records = [{"vers": "1.0.0"}]
        self.assertIsNone(choose_record(records, "2.0.0"))


if __name__ == "__main__":
    unittest.main()
