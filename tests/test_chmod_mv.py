"""Тесты для команд chmod и mv."""

import zipfile

from src.commands import handle_chmod, handle_mv
from src.vfs import Vfs, VfsFile


def _vfs_with_file() -> Vfs:
    """VFS с одним файлом file.txt."""
    vfs = Vfs()
    vfs.root.children["file.txt"] = VfsFile("file.txt", b"data")
    vfs.current = vfs.root
    return vfs


def test_chmod_sets_mode():
    """chmod меняет права."""
    vfs = _vfs_with_file()
    handle_chmod(vfs, ["755", "file.txt"])
    assert vfs.root.children["file.txt"].mode == "755"


def test_chmod_missing_file():
    """chmod на несуществующем — ошибка."""
    vfs = Vfs()
    assert "Ошибка" in handle_chmod(vfs, ["755", "missing.txt"])


def test_chmod_without_args():
    """chmod без аргументов — ошибка."""
    vfs = Vfs()
    assert "Ошибка" in handle_chmod(vfs, [])


def test_mv_renames_file():
    """mv переименовывает файл."""
    vfs = _vfs_with_file()
    handle_mv(vfs, ["file.txt", "new.txt"])
    assert "file.txt" not in vfs.root.children
    assert "new.txt" in vfs.root.children


def test_mv_missing_source():
    """mv с несуществующим источником — ошибка."""
    vfs = Vfs()
    assert "Ошибка" in handle_mv(vfs, ["missing", "new.txt"])
