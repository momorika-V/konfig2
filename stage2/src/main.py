"""Этап 2: сбор данных — прямые зависимости пакета.

Данные берутся из sparse-индекса crates.io напрямую через HTTP,
без менеджеров пакетов и сторонних библиотек.
"""

from config import build_parser, validate_config
from fetcher import direct_dependencies

ERROR_EXIT_CODE = 1


def run(config):
    """Выводит все прямые зависимости заданного пакета."""
    errors = validate_config(config)
    for message in errors:
        print(f"Ошибка: {message}")
    if errors:
        return ERROR_EXIT_CODE
    if config.test_mode:
        print("Режим тестирования будет поддержан на этапе 3.")
        return 0
    try:
        deps = direct_dependencies(config.package, config.version)
    except (ValueError, OSError) as exc:
        print(f"Ошибка получения данных: {exc}")
        return ERROR_EXIT_CODE
    print(f"Прямые зависимости {config.package}:")
    for name, requirement in deps:
        print(f"  {name} ({requirement})")
    if not deps:
        print("  (зависимостей нет)")
    return 0


def main():
    """Точка входа приложения."""
    config = build_parser().parse_args()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
