"""Этап 1: минимальный прототип с конфигурацией.

Приложение разбирает параметры командной строки, выводит их в формате
ключ-значение и демонстрирует обработку ошибок для каждого параметра.
"""

from config import build_parser, validate_config

ERROR_EXIT_CODE = 1


def print_config(config):
    """Печатает все параметры запуска в формате ключ-значение."""
    print("Параметры запуска:")
    for key, value in vars(config).items():
        print(f"  {key} = {value}")


def run(config):
    """Выполняет приложение в соответствии с параметрами."""
    print_config(config)
    errors = validate_config(config)
    for message in errors:
        print(f"Ошибка: {message}")
    return ERROR_EXIT_CODE if errors else 0


def main():
    """Точка входа приложения."""
    config = build_parser().parse_args()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
