"""Тесты для команд-заглушек"""

from src.commands import COMMANDS, handle_cd, handle_ls


def test_ls_returns_name_and_args():
    """ls возвращает своё имя и аргументы"""
    result = handle_ls(["-la", "/home"])
    assert "ls" in result
    assert "-la" in result
    assert "/home" in result


def test_cd_returns_name_and_args():
    """cd возвращает своё имя и аргументы"""
    result = handle_cd(["/tmp"])
    assert "cd" in result
    assert "/tmp" in result


def test_commands_dict_contains_ls_and_cd():
    """Словарь команд содержит ls и cd"""
    assert "ls" in COMMANDS
    assert "cd" in COMMANDS
    assert COMMANDS["ls"] is handle_ls
    assert COMMANDS["cd"] is handle_cd