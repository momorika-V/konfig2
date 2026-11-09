"""Визуализация графа зависимостей: PlantUML и PNG.

Текст диаграммы PlantUML формируется из графа. PNG-изображение
получается с сервера PlantUML: диаграмма сжимается zlib и кодируется
в URL-совместимую строку (стандартная библиотека, без сторонних
зависимостей).
"""

import urllib.request
import zlib

SERVER_URL = "http://www.plantuml.com/plantuml/png/"

USER_AGENT = "pr22-dependency-viewer (student project)"

HEADER = "@startuml"

FOOTER = "@enduml"
TWO_BYTES = 2

THREE_BYTES = 3
DEFLATE_HEAD = 2
DEFLATE_TAIL = 4
ALPHABET = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz-_"
)


def plantuml_text(graph):
    """Собирает текст диаграммы PlantUML по графу зависимостей."""
    lines = [HEADER]
    for name in sorted(graph):
        for dep in graph[name]:
            lines.append(f"{name} --> {dep}")
    lines.append(FOOTER)
    return "\n".join(lines)


def encode_plantuml(text):
    """Кодирует диаграмму в строку для URL сервера PlantUML."""
    compressed = zlib.compress(text.encode("utf-8"))

    return encode_bytes(compressed[DEFLATE_HEAD:-DEFLATE_TAIL])


def encode_bytes(data):

    """Кодирует байты группами по три в четыре символа."""

    result = []

    for index in range(0, len(data), THREE_BYTES):

        result.append(encode_chunk(data[index:index + THREE_BYTES]))

    return "".join(result)





def encode_chunk(chunk):

    """Кодирует 1–3 байта в четыре символа алфавита PlantUML."""

    first = chunk[0]

    second = chunk[1] if len(chunk) >= TWO_BYTES else 0

    third = chunk[2] if len(chunk) >= THREE_BYTES else 0
    values = [
        first >> 2,
        ((first & 0x3) << 4) | (second >> 4),
        ((second & 0xF) << 2) | (third >> 6),
        third & 0x3F,
    ]
    return "".join(ALPHABET[value] for value in values)


def save_text(text, file_name):
    """Сохраняет текст диаграммы в файл .puml."""
    with open(file_name, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")


def save_png(graph, file_name):

    """Сохраняет PNG-изображение графа через сервер PlantUML."""

    url = SERVER_URL + encode_plantuml(plantuml_text(graph))

    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        image = response.read()
    with open(file_name, "wb") as handle:
        handle.write(image)
