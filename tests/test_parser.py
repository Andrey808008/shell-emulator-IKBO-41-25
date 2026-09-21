"""Тесты для парсера команд"""

from src.parser import parse_command


def test_empty_string():
    """Пустая строка = пустой результат"""
    assert parse_command("") == ("", [])


def test_only_spaces():
    """Только пробелы = пустой результат"""
    assert parse_command("   ") == ("", [])


def test_command_without_args():
    """Команда без аргументов"""
    assert parse_command("ls") == ("ls", [])


def test_command_with_one_arg():
    """Команда с одним аргументом"""
    assert parse_command("cd /tmp") == ("cd", ["/tmp"])


def test_command_with_many_args():
    """Команда с несколькими аргументами"""
    assert parse_command("ls -la /home") == ("ls", ["-la", "/home"])


def test_extra_spaces():
    """Лишние пробелы игнорируются"""
    assert parse_command("  ls   -la  ") == ("ls", ["-la"])