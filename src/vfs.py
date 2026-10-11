"""Виртуальная файловая система (VFS)."""

import io
import zipfile
from pathlib import Path


class VfsNode:
    """Базовый узел VFS: файл или директория."""

    def __init__(self, name: str) -> None:
        """Сохраняет имя узла."""
        self.name = name


class VfsFile(VfsNode):
    """Файл в VFS."""

    def __init__(self, name: str, content: bytes = b"") -> None:
        """Сохраняет имя и содержимое файла."""
        super().__init__(name)
        self.content = content


class VfsDirectory(VfsNode):
    """Директория в VFS."""

    def __init__(self, name: str) -> None:
        """Создаёт пустую директорию."""
        super().__init__(name)
        self.children: dict[str, VfsNode] = {}


class Vfs:
    """Виртуальная файловая система в памяти."""

    def __init__(self) -> None:
        """Создаёт VFS по умолчанию (пустой корень)."""
        self.root = VfsDirectory("/")
        self.current = self.root

    def load_zip(self, zip_path: str) -> None:
        """
        Загружает содержимое ZIP-архива в VFS (без распаковки на диск).

        :param zip_path: Путь к ZIP-архиву.
        """
        self.root = VfsDirectory("/")
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                data = zf.read(info.filename)
                self._add_file(info.filename, data)
        self.current = self.root

    def _add_file(self, path: str, data: bytes) -> None:
        """Добавляет файл по пути, создавая промежуточные папки."""
        parts = path.replace("\\", "/").split("/")
        node = self.root
        for part in parts[:-1]:
            if part not in node.children:
                node.children[part] = VfsDirectory(part)
            node = node.children[part]
        node.children[parts[-1]] = VfsFile(parts[-1], data)

    def _parent_of(self, node: VfsDirectory) -> VfsDirectory:
        """Ищет родителя узла обходом дерева."""
        return self._find_parent(self.root, node)

    def _find_parent(
        self,
        current: VfsDirectory,
        target: VfsDirectory,
    ) -> VfsDirectory:
        """Рекурсивно ищет родителя target."""
        for child in current.children.values():
            if child is target:
                return current
            if isinstance(child, VfsDirectory):
                result = self._find_parent(child, target)
                if result is not None:
                    return result
        return self.root