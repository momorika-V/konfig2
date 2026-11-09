"""Тесты визуализации графа (этап 5)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual import (

    encode_bytes, encode_chunk, encode_plantuml, plantuml_text)



GRAPH = {"A": ["B", "C"], "B": [], "C": []}
CHUNK_CHARS = 4
TWO_CHUNKS = 8


class PlantumlTextTest(unittest.TestCase):
    """Сборка текста диаграммы PlantUML."""

    def test_text_content(self):
        """Диаграмма содержит каркас и стрелки графа."""
        text = plantuml_text(GRAPH)
        lines = text.splitlines()
        self.assertEqual(lines[0], "@startuml")
        self.assertEqual(lines[-1], "@enduml")
        self.assertIn("A --> B", lines)
        self.assertIn("A --> C", lines)

    def test_sorted_packages(self):

        """Пакеты перечисляются в алфавитном порядке."""

        graph = {"C": ["A"], "B": ["A"], "A": []}
        text = plantuml_text(graph)

        self.assertLess(text.index("B -->"), text.index("C -->"))


class EncodeTest(unittest.TestCase):
    """Кодирование диаграммы для URL сервера PlantUML."""

    def test_encode_chunk_padding(self):
        """Короткий блок дополняется нулями до четырёх символов."""
        self.assertEqual(len(encode_chunk(b"\x01")), CHUNK_CHARS)
        self.assertEqual(encode_chunk(b"\x00\x00\x00"), "0000")

    def test_encode_bytes_length(self):
        """Каждые три байта дают ровно четыре символа."""
        self.assertEqual(len(encode_bytes(b"abc")), CHUNK_CHARS)

        self.assertEqual(len(encode_bytes(b"abcde")), TWO_CHUNKS)

    def test_encode_plantuml_ascii(self):
        """Результат кодирования состоит из ASCII-символов."""
        encoded = encode_plantuml(plantuml_text(GRAPH))
        self.assertTrue(encoded.isascii())


if __name__ == "__main__":
    unittest.main()
