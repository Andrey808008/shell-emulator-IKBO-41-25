"""Обработчики команд-заглушек"""


def handle_ls(args: list[str]) -> str:
    """ls - своё имя и аргументы"""
    return f"Выполнена команда: ls, аргументы: {args}"


def handle_cd(args: list[str]) -> str:
    """cd - своё имя и аргументы"""
    return f"Выполнена команда: cd, аргументы: {args}"


"""команды"""
COMMANDS = {
    "ls": handle_ls,
    "cd": handle_cd,
}