"""Этап 4: дополнительные операции — порядок загрузки зависимостей.

Сначала строится граф (этап 3), затем выводится порядок загрузки:
зависимости всегда раньше пакетов, которые от них зависят.
"""

from config import build_parser, validate_config
from graph import (
    CargoLoader, TestRepoLoader, build_graph, print_graph)
from order import load_order, print_order

ERROR_EXIT_CODE = 1


def make_loader(config):
    """Создаёт источник данных в зависимости от режима работы."""
    if config.test_mode:
        return TestRepoLoader(config.url)
    return CargoLoader(config.package, config.version)


def run(config):
    """Строит граф и печатает порядок загрузки зависимостей."""
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
    print_order(load_order(graph, config.package))
    return 0


def main():
    """Точка входа приложения."""
    config = build_parser().parse_args()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
