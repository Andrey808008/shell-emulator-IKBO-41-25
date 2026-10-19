"""Обработчики команд эмулятора."""

from src.vfs import Vfs, VfsDirectory, VfsFile

# Константы (убирают магические числа)
MAX_HEAD_LINES = 10
BYTES_IN_KB = 1024
BYTES_IN_MB = 1024 * 1024
DEFAULT_FILE_MODE = "644"


def _parse_ls_flags(args: list[str]) -> tuple[bool, bool, bool]:
    """Извлекает флаги -a, -l, -h из аргументов."""
    show_hidden = False
    long_format = False
    human = False
    for arg in args:
        if arg.startswith("-") and len(arg) > 1:
            for ch in arg[1:]:
                if ch == "a":
                    show_hidden = True
                elif ch == "l":
                    long_format = True
                elif ch == "h":
                    human = True
    return show_hidden, long_format, human


def _format_size(size: int, human: bool) -> str:
    """Форматирует размер файла."""
    if not human:
        return str(size)
    if size < BYTES_IN_KB:
        return f"{size}B"
    if size < BYTES_IN_MB:
        return f"{size // BYTES_IN_KB}K"
    return f"{size // BYTES_IN_MB}M"


def _format_long_item(name: str, node, human: bool) -> str:
    """Форматирует одну строку для режима ls -l."""
    is_dir = isinstance(node, VfsDirectory)
    kind = "d" if is_dir else "-"
    mode = getattr(node, "mode", DEFAULT_FILE_MODE)
    size_str = "-" if is_dir else _format_size(len(node.content), human)
    return f"{kind}{mode}  {size_str:>8}  {name}"


def handle_ls(vfs: Vfs, args: list[str]) -> str:
    """Показывает содержимое текущей директории с учётом флагов."""
    show_hidden, long_format, human = _parse_ls_flags(args)

    items = sorted(vfs.current.children.items())
    if not show_hidden:
        items = [(n, node) for n, node in items if not n.startswith(".")]

    if not items:
        return "(пусто)"

    if not long_format:
        return "  ".join(name for name, _ in items)

    lines = [_format_long_item(name, node, human) for name, node in items]
    return "\n".join(lines)


def handle_cd(vfs: Vfs, args: list[str]) -> str:
    """Меняет текущую директорию, поддерживая пути через /, . и .."""
    if not args:
        return "Ошибка: cd требует аргумент"

    path = args[0]
    node = vfs.root if path.startswith("/") else vfs.current

    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            node = vfs._parent_of(node)
            continue
        nxt = node.children.get(segment)
        if nxt is None or not isinstance(nxt, VfsDirectory):
            return f"Ошибка: '{segment}' не найдено"
        node = nxt

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
    """Выводит первые MAX_HEAD_LINES строк файла."""
    if not args:
        return "Ошибка: head требует аргумент"
    node = vfs.current.children.get(args[0])
    if not isinstance(node, VfsFile):
        return f"Ошибка: '{args[0]}' не найден"
    lines = node.content.decode("utf-8", errors="replace").splitlines()
    return "\n".join(lines[:MAX_HEAD_LINES])


def handle_chmod(vfs: Vfs, args: list[str]) -> str:
    """Меняет права доступа к файлу."""
    if len(args) < 2:
        return "Ошибка: chmod требует режим и имя файла"
    mode, name = args[0], args[1]
    node = vfs.current.children.get(name)
    if node is None:
        return f"Ошибка: '{name}' не найден"
    node.mode = mode
    return ""


def handle_mv(vfs: Vfs, args: list[str]) -> str:
    """Перемещает или переименовывает файл."""
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