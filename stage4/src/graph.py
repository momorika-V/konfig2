"""Построение графа зависимостей обходом DFS без рекурсии.

Поддержаны два источника данных: sparse-индекс crates.io и файл
описания тестового репозитория (пакеты — заглавные латинские буквы).
"""

from config import DEFAULT_VERSION
from fetcher import direct_dependencies

TEST_COMMENT = "#"


class TestRepoLoader:
    """Источник данных: файл описания тестового репозитория.

    Формат файла: каждая строка 'A: B, C' означает, что пакет A
    зависит от B и C; строки с # и пустые игнорируются.
    """

    def __init__(self, path):
        self.graph = load_test_graph(path)

    def get_deps(self, name):
        """Возвращает список зависимостей пакета."""
        return self.graph.get(name, [])


class CargoLoader:
    """Источник данных: sparse-индекс crates.io."""

    def __init__(self, root_name, root_version):
        self.root_name = root_name
        self.root_version = root_version

    def get_deps(self, name):
        """Возвращает имена зависимостей пакета.

        Заданная пользователем версия применяется только к корневому
        пакету; остальные пакеты берутся последней версией.
        """
        if name == self.root_name:
            version = self.root_version
        else:
            version = DEFAULT_VERSION
        return [dep for dep, _ in direct_dependencies(name, version)]


def load_test_graph(path):
    """Читает описание тестового репозитория в словарь графов."""
    graph = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            add_test_line(graph, line)
    return graph


def add_test_line(graph, line):
    """Разбирает одну строку файла тестового репозитория."""
    line = line.strip()
    if not line or line.startswith(TEST_COMMENT):
        return
    name, deps_text = line.split(":", 1)
    deps = [d.strip() for d in deps_text.split(",") if d.strip()]
    graph[name.strip()] = deps


def is_excluded(name, filter_sub):
    """Определяет, исключён ли пакет фильтром по подстроке."""
    return bool(filter_sub) and filter_sub in name


def build_graph(start, loader, filter_sub):
    """Строит граф зависимостей итеративным DFS от начального пакета.

    Возвращает словарь {пакет: [зависимости]}. Пакеты, имя которых
    содержит подстроку фильтра, в анализ не попадают. Уже посещённые
    пакеты не обрабатываются повторно, поэтому циклы безопасны.
    """
    graph = {}
    visited = set()
    stack = [start]
    while stack:
        name = stack.pop()
        if name in visited:
            continue
        visited.add(name)
        deps = [dep for dep in loader.get_deps(name)
                if not is_excluded(dep, filter_sub)]
        graph[name] = deps
        stack.extend(dep for dep in deps if dep not in visited)
    return graph


def print_graph(graph):
    """Печатает граф построчно в виде 'пакет -> зависимости'."""
    for name in sorted(graph):
        deps = ", ".join(graph[name]) if graph[name] else "-"
        print(f"{name} -> {deps}")
