"""Обработчики команд эмулятора."""

from src.vfs import Vfs, VfsDirectory, VfsFile

def handle_ls(vfs: Vfs, args: list[str]) -> str:
    """Показывает содержимое текущей директории VFS."""
    if args:
        name = args[0]
        if name in vfs.current.children:
            node = vfs.current.children[name]
            if isinstance(node, VfsDirectory):
                items = sorted(node.children.keys())
                return "  ".join(items) if items else "(пусто)"
            return name
        return f"Ошибка: '{name}' не найдено"

    items = sorted(vfs.current.children.keys())
    return "  ".join(items) if items else "(пусто)"


def handle_cd(vfs: Vfs, args: list[str]) -> str:
    """Меняет текущую директорию VFS."""
    if not args:
        return "Ошибка: cd требует аргумент"

    target = args[0]

    if target == "/":
        vfs.current = vfs.root
        return ""

    if target == "..":
        vfs.current = vfs._parent_of(vfs.current)
        return ""

    node = vfs.current.children.get(target)
    if node is None or not isinstance(node, VfsDirectory):
        return f"Ошибка: '{target}' не найдено"

    vfs.current = node
    return ""

def handle_tac(vfs: Vfs, args: list[str]) -> str:
    """Выводит содержимое файла в обратном порядке строк."""
    if not args:
        return "Ошибка: tac требует аргумент"
    node = vfs.current.children.get(args[0])
    if not isinstance(node, VfsFile):
        return f"Ошибка: '{args[0]}' не найден"
    lines = node.content.decode("utf-8", errors="replace").splitlines()
    return "\n".join(reversed(lines))


def handle_head(vfs: Vfs, args: list[str]) -> str:
    """Выводит первые 10 строк файла."""
    if not args:
        return "Ошибка: head требует аргумент"
    node = vfs.current.children.get(args[0])
    if not isinstance(node, VfsFile):
        return f"Ошибка: '{args[0]}' не найден"
    lines = node.content.decode("utf-8", errors="replace").splitlines()
    return "\n".join(lines[:10])

def handle_chmod(vfs: Vfs, args: list[str]) -> str:
    """Меняет права доступа к файлу (сохраняет в атрибуте)."""
    if len(args) < 2:
        return "Ошибка: chmod требует режим и имя файла"
    mode, name = args[0], args[1]
    node = vfs.current.children.get(name)
    if node is None:
        return f"Ошибка: '{name}' не найден"
    node.mode = mode
    return ""


def handle_mv(vfs: Vfs, args: list[str]) -> str:
    """Перемещает или переименовывает файл внутри текущей папки."""
    if len(args) < 2:
        return "Ошибка: mv требует источник и назначение"
    src, dst = args[0], args[1]
    node = vfs.current.children.get(src)
    if node is None:
        return f"Ошибка: '{src}' не найден"
    del vfs.current.children[src]
    node.name = dst
    vfs.current.children[dst] = node
    return ""

COMMANDS = {
    "ls": handle_ls,
    "cd": handle_cd,
    "tac": handle_tac,
    "head": handle_head,
    "chmod": handle_chmod,
    "mv": handle_mv,
}