"""Разбор параметров командной строки эмулятора"""

import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки. Вариант 18."
    )
    parser.add_argument(
        "--vfs",
        type=str,
        default=None,
        help="Путь к физическому расположению VFS (ZIP-архив).",
    )
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Путь к CSV-файлу для логирования команд.",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Путь к стартовому скрипту с командами.",
    )
    return parser.parse_args()