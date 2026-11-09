"""Разбор и проверка параметров командной строки приложения."""

import os
import re
import argparse

DEFAULT_VERSION = "latest"
DEFAULT_OUTPUT = "graph.png"

PACKAGE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,95}$")
TEST_PACKAGE_PATTERN = re.compile(r"^[A-Z]$")
VERSION_PATTERN = re.compile(r"^\d+(\.\d+){0,3}$")


def build_parser():
    """Создаёт парсер опций командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей Cargo.")
    parser.add_argument(
        "--package", default="",
        help="имя анализируемого пакета")
    parser.add_argument(
        "--url", default="",
        help="URL репозитория или путь к тестовому файлу")
    parser.add_argument(
        "--test-mode", action="store_true",
        help="работа с тестовым репозиторием")
    parser.add_argument(
        "--version", default=DEFAULT_VERSION,
        help="версия пакета (по умолчанию latest)")
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT,
        help="имя файла с изображением графа")
    parser.add_argument(
        "--filter", default="",
        help="подстрока для исключения пакетов из анализа")
    return parser


def validate_config(config):
    """Проверяет параметры и возвращает список сообщений об ошибках."""
    errors = check_package(config.package, config.test_mode)
    errors += check_url(config.url, config.test_mode)
    errors += check_version(config.version)
    errors += check_output(config.output)
    return errors


def check_package(package, test_mode):
    """Проверяет имя пакета (в тестовом режиме — одна буква A-Z)."""
    if not package:
        return ["не задано имя пакета (--package)"]
    if test_mode and TEST_PACKAGE_PATTERN.match(package):
        return []
    if not PACKAGE_PATTERN.match(package):
        return ["недопустимое имя пакета: " + package]
    return []


def check_url(url, test_mode):
    """Проверяет адрес репозитория или путь к тестовому файлу."""
    if not url:
        return ["не задан URL репозитория или путь к файлу (--url)"]
    if test_mode and not os.path.isfile(url):
        return ["файл тестового репозитория не найден: " + url]
    return []


def check_version(version):
    """Проверяет строку версии пакета."""
    if version == DEFAULT_VERSION:
        return []
    if not VERSION_PATTERN.match(version):
        return ["недопустимая версия: " + version]
    return []


def check_output(output):
    """Проверяет имя файла с изображением графа."""
    if not output.lower().endswith(".png"):
        return ["файл изображения должен иметь расширение .png"]
    return []
