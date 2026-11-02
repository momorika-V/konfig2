"""Тесты разбора и проверки параметров командной строки."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import build_parser, validate_config


class ConfigTest(unittest.TestCase):
    """Проверки корректных и ошибочных параметров запуска."""

    def test_default_values(self):
        """Без аргументов парсер подставляет значения по умолчанию."""
        config = build_parser().parse_args([])
        self.assertEqual(config.version, "latest")
        self.assertEqual(config.output, "graph.png")
        self.assertFalse(config.test_mode)

    def test_valid_config(self):
        """Корректный набор параметров не даёт ошибок."""
        config = build_parser().parse_args(
            ["--package", "serde", "--url", "https://index.crates.io"])
        self.assertEqual(validate_config(config), [])

    def test_empty_package(self):
        """Пустое имя пакета фиксируется как ошибка."""
        config = build_parser().parse_args([])
        errors = validate_config(config)
        self.assertTrue(any("package" in text for text in errors))

    def test_bad_package_name(self):
        """Имя пакета с недопустимыми символами отклоняется."""
        config = build_parser().parse_args(
            ["--package", "Serde!", "--url", "https://x"])
        errors = validate_config(config)
        self.assertTrue(any("имя пакета" in text for text in errors))

    def test_bad_version(self):
        """Некорректная версия пакета отклоняется."""
        config = build_parser().parse_args(
            ["--package", "serde", "--url", "https://x",
             "--version", "1.a"])
        errors = validate_config(config)
        self.assertTrue(any("версия" in text for text in errors))

    def test_bad_output(self):
        """Имя файла изображения без .png отклоняется."""
        config = build_parser().parse_args(
            ["--package", "serde", "--url", "https://x",
             "--output", "graph.jpg"])
        errors = validate_config(config)
        self.assertTrue(any("png" in text for text in errors))

    def test_test_mode_missing_file(self):
        """В тестовом режиме путь должен указывать на существующий файл."""
        config = build_parser().parse_args(
            ["--package", "A", "--test-mode", "--url", "no_such.txt"])
        errors = validate_config(config)
        self.assertTrue(any("не найден" in text for text in errors))


if __name__ == "__main__":
    unittest.main()
