"""Модуль для настройки интерфейса командной строки и точки входа."""
import argparse
import sys
import os


def parse_arguments():
    """Разбирает и возвращает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализатор графа зависимостей Maven"
    )
    parser.add_argument(
        "-p", "--package", required=True,
        help="Имя пакета (groupId:artifactId)"
    )
    parser.add_argument(
        "-u", "--url", required=True,
        help="URL репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true",
        help="Режим работы с тестовым файлом"
    )
    parser.add_argument(
        "-v", "--version", required=True,
        help="Версия анализируемого пакета"
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=10,
        help="Максимальная глубина анализа"
    )
    parser.add_argument(
        "-f", "--filter", default="",
        help="Подстрока для фильтрации пакетов"
    )
    return parser.parse_args()


def validate_args(args):
    """Проверяет корректность переданных параметров."""
    if not args.package or ":" not in args.package:
        print("Ошибка: Пакет должен быть в формате 'groupId:artifactId'")
        sys.exit(1)

    if not args.test_mode and not args.url.startswith("http"):
        print("Ошибка: URL должен начинаться с http в обычном режиме")
        sys.exit(1)

    if args.test_mode and not os.path.exists(args.url):
        print(f"Ошибка: Тестовый файл не найден по пути {args.url}")
        sys.exit(1)

    if args.depth <= 0:
        print("Ошибка: Глубина должна быть больше 0")
        sys.exit(1)


def print_config(args):
    """Выводит все настраиваемые параметры в формате ключ-значение."""
    print("--- Конфигурация ---")
    print(f"Пакет:        {args.package}")
    print(f"URL/Путь:     {args.url}")
    print(f"Тест-режим:   {args.test_mode}")
    print(f"Версия:       {args.version}")
    print(f"Глубина:      {args.depth}")
    print(f"Фильтр:       {args.filter}")
    print("--------------------")


def main():
    """Главная точка входа в приложение."""
    args = parse_arguments()
    validate_args(args)
    print_config(args)


if __name__ == "__main__":
    main()