"""Тесты для команд ls и cd."""

from src.commands import COMMANDS, handle_cd, handle_ls
from src.vfs import Vfs


def test_ls_empty_vfs():
    """ls на пустой VFS возвращает '(пусто)'."""
    vfs = Vfs()
    result = handle_ls(vfs, [])
    assert result == "(пусто)"


def test_cd_requires_argument():
    """cd без аргумента — ошибка."""
    vfs = Vfs()
    result = handle_cd(vfs, [])
    assert "Ошибка" in result


def test_cd_to_missing_directory():
    """cd в несуществующую папку — ошибка."""
    vfs = Vfs()
    result = handle_cd(vfs, ["missing"])
    assert "Ошибка" in result


def test_cd_to_root():
    """cd / — переход в корень."""
    vfs = Vfs()
    result = handle_cd(vfs, ["/"])
    assert result == ""
    assert vfs.current is vfs.root


def test_commands_dict_contains_ls_and_cd():
    """Словарь команд содержит ls и cd."""
    assert "ls" in COMMANDS
    assert "cd" in COMMANDS
    assert COMMANDS["ls"] is handle_ls
    assert COMMANDS["cd"] is handle_cd