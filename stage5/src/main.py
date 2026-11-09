"""Этап 5: визуализация графа зависимостей.

Формируется текстовое представление графа на языке PlantUML, текст
сохраняется в .puml, изображение — в PNG (параметр --output).
"""

from config import build_parser, validate_config
from graph import (
    CargoLoader, TestRepoLoader, build_graph, print_graph)
from visual import plantuml_text, save_png, save_text

ERROR_EXIT_CODE = 1

PUML_SUFFIX = ".puml"
PNG_SUFFIX_LEN = 4


def make_loader(config):
    """Создаёт источник данных в зависимости от режима работы."""
    if config.test_mode:
        return TestRepoLoader(config.url)
    return CargoLoader(config.package, config.version)


def save_diagram(graph, output_name):
    """Сохраняет .puml и, если удалось, PNG с изображением графа."""
    text_name = output_name[:-PNG_SUFFIX_LEN] + PUML_SUFFIX
    text = plantuml_text(graph)
    save_text(text, text_name)
    print(f"Текст диаграммы PlantUML:\n{text}")
    print(f"Сохранено: {text_name}")
    try:
        save_png(graph, output_name)
        print(f"Изображение сохранено: {output_name}")
    except OSError as exc:
        print(f"PNG недоступен ({exc}); используйте .puml "
              f"или сайт plantuml.com")


def run(config):
    """Строит граф, печатает его и сохраняет диаграмму."""
    errors = validate_config(config)
    for message in errors:
        print(f"Ошибка: {message}")
    if errors:
        return ERROR_EXIT_CODE
    try:
        graph = build_graph(
            config.package, make_loader(config), config.filter)
    except (ValueError, OSError) as exc:
        print(f"Ошибка получения данных: {exc}")
        return ERROR_EXIT_CODE
    print_graph(graph)
    save_diagram(graph, config.output)
    return 0


def main():
    """Точка входа приложения."""
    config = build_parser().parse_args()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
