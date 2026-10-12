"""Тесты для виртуальной файловой системы."""

import zipfile

from src.vfs import Vfs, VfsDirectory, VfsFile


def test_empty_vfs():
    """Пустая VFS: корень без детей."""
    vfs = Vfs()
    assert vfs.current is vfs.root
    assert len(vfs.root.children) == 0


def test_load_zip_creates_files(tmp_path):
    """Загрузка ZIP создаёт файлы и папки."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("a.txt", "hello")
        zf.writestr("sub/b.txt", "world")

    vfs = Vfs()
    vfs.load_zip(str(zip_path))

    assert "a.txt" in vfs.root.children
    assert "sub" in vfs.root.children

    sub = vfs.root.children["sub"]
    assert isinstance(sub, VfsDirectory)
    assert "b.txt" in sub.children


def test_load_zip_file_content(tmp_path):
    """Содержимое файла сохраняется."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("a.txt", "hello")

    vfs = Vfs()
    vfs.load_zip(str(zip_path))

    a_file = vfs.root.children["a.txt"]
    assert isinstance(a_file, VfsFile)
    assert a_file.content == b"hello"


def test_deep_nesting(tmp_path):
    """Вложенные папки создаются автоматически."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("l1/l2/l3/deep.txt", "deep")

    vfs = Vfs()
    vfs.load_zip(str(zip_path))

    l1 = vfs.root.children["l1"]
    l2 = l1.children["l2"]
    l3 = l2.children["l3"]
    assert "deep.txt" in l3.children


def test_parent_of_root():
    """Родитель корня — сам корень."""
    vfs = Vfs()
    assert vfs._parent_of(vfs.root) is vfs.root


def test_parent_of_child(tmp_path):
    """Родитель вложенной папки находится правильно."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("sub/a.txt", "x")

    vfs = Vfs()
    vfs.load_zip(str(zip_path))

    sub = vfs.root.children["sub"]
    assert vfs._parent_of(sub) is vfs.root