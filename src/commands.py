"""Обработчики команд эмулятора."""

from src.vfs import Vfs, VfsDirectory, VfsFile

def handle_ls(vfs: Vfs, args: list[str]) -> str:
    """Показывает содержимое текущей директории с учётом флагов -l, -a, -h."""
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

    items = sorted(vfs.current.children.items())

    if not show_hidden:
        items = [(n, node) for n, node in items if not n.startswith(".")]

    if not items:
        return "(пусто)"

    if not long_format:
        return "  ".join(name for name, _ in items)

    lines = []
    for name, node in items:
        is_dir = isinstance(node, VfsDirectory)
        kind = "d" if is_dir else "-"
        mode = getattr(node, "mode", "644")
        if is_dir:
            size = "-"
        else:
            size = _format_size(len(node.content), human)
        lines.append(f"{kind}{mode}  {size:>8}  {name}")
    return "\n".join(lines)


def _format_size(size: int, human: bool) -> str:
    """Форматирует размер файла."""
    if not human:
        return str(size)
    if size < 1024:
        return f"{size}B"
    if size < 1024 * 1024:
        return f"{size // 1024}K"
    return f"{size // (1024 * 1024)}M"


def handle_cd(vfs: Vfs, args: list[str]) -> str:
    """Меняет текущую директорию, поддерживая пути через /, . и .."""
    if not args:
        return "Ошибка: cd требует аргумент"

    path = args[0]

    if path.startswith("/"):
        node = vfs.root
    else:
        node = vfs.current

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