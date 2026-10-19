"""Тесты для команд head и tac."""

import io
import zipfile
MAX_LINES = 10

from src.commands import handle_head, handle_tac, MAX_HEAD_LINES
from src.vfs import Vfs


def _vfs_with_file(content: str) -> Vfs:
    """Готовит VFS с одним файлом file.txt."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("file.txt", content)
    buf.seek(0)
    vfs = Vfs()
    with zipfile.ZipFile(buf, "r") as zf:
        for info in zf.infolist():
            if not info.is_dir():
                vfs._add_file(info.filename, zf.read(info.filename))
    return vfs


def test_head_returns_first_lines():
    """head возвращает первые строки."""
    vfs = _vfs_with_file("a\nb\nc\nd")
    result = handle_head(vfs, ["file.txt"])
    assert result == "a\nb\nc\nd"


def test_head_limits_to_ten_lines():
    """head обрезает до 10 строк."""
    content = "\n".join(str(i) for i in range(20))
    vfs = _vfs_with_file(content)
    result = handle_head(vfs, ["file.txt"])
    assert len(result.splitlines()) == MAX_LINES


def test_tac_reverses_lines():
    """tac переворачивает порядок строк."""
    vfs = _vfs_with_file("a\nb\nc")
    result = handle_tac(vfs, ["file.txt"])
    assert result == "c\nb\na"


def test_head_without_args():
    """head без аргумента — ошибка."""
    vfs = Vfs()
    assert "Ошибка" in handle_head(vfs, [])


def test_tac_missing_file():
    """tac на несуществующем файле — ошибка."""
    vfs = Vfs()
    assert "Ошибка" in handle_tac(vfs, ["missing.txt"])