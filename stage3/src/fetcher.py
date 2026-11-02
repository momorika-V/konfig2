"""Получение данных о пакете из sparse-индекса crates.io."""

import json
import urllib.request

from config import DEFAULT_VERSION

INDEX_URL = "https://index.crates.io/"
USER_AGENT = "pr22-dependency-viewer (student project)"
NORMAL_KIND = "normal"

LATEST = DEFAULT_VERSION

PATH_LEN_SINGLE = 1

PATH_LEN_DOUBLE = 2

PATH_LEN_TRIPLE = 3
PATH_SEG_LEN = 2


def index_path(name):
    """Строит путь пакета в sparse-индексе crates.io."""

    if len(name) == PATH_LEN_SINGLE:

        return f"1/{name}"

    if len(name) == PATH_LEN_DOUBLE:

        return f"2/{name}"

    if len(name) == PATH_LEN_TRIPLE:

        return f"3/{name[0]}/{name}"
    return (f"{name[:PATH_SEG_LEN]}/"
            f"{name[PATH_SEG_LEN:PATH_SEG_LEN * 2]}/{name}")


def fetch_records(name):
    """Загружает и разбирает записи обо всех версиях пакета."""
    url = INDEX_URL + index_path(name)
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        text = response.read().decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def parse_version(version):
    """Преобразует строку версии в кортеж чисел для сравнения."""
    return tuple(int(part) for part in version.split("."))


def choose_record(records, version):
    """Выбирает запись нужной версии (latest — самая новая)."""
    if version == LATEST:
        return max(records, key=lambda record: parse_version(
            record["vers"]))
    for record in records:
        if record["vers"] == version:
            return record
    return None


def direct_dependencies(name, version):
    """Возвращает прямые зависимости: список пар (имя, требование)."""
    record = choose_record(fetch_records(name), version)
    if record is None:
        raise ValueError(f"версия {version} пакета {name} не найдена")
    deps = []
    for dep in record.get("deps", []):
        if dep.get("kind", NORMAL_KIND) != NORMAL_KIND:
            continue
        deps.append((dep["name"], dep.get("req", "")))
    return deps
