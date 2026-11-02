"""Этап 3: построение графа зависимостей (DFS без рекурсии).

Реальный репозиторий (crates.io) и тестовый файл обрабатываются
одним алгоритмом через разные источники данных.
"""

from config import build_parser, validate_config
from graph import (
    CargoLoader, TestRepoLoader, build_graph, print_graph)

ERROR_EXIT_CODE = 1


def make_loader(config):
    """Создаёт источник данных в зависимости от режима работы."""
    if config.test_mode:
        return TestRepoLoader(config.url)
    return CargoLoader(config.package, config.version)


def run(config):
    """Строит граф зависимостей и печатает его."""
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
    return 0


def main():
    """Точка входа приложения."""
    config = build_parser().parse_args()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
