"""Выполнение стартового скрипта с командами эмулятора."""

from pathlib import Path

from src.commands import COMMANDS
from src.logger import Logger
from src.parser import parse_command


class ScriptRunner:
    """Выполняет команды из файла-скрипта."""

    def __init__(self, logger: Logger) -> None:
        """Инициализирует исполнитель скрипта."""
        self.logger = logger

    def run(self, script_path: str, output_func, vfs) -> None:
        """
        Выполняет все команды из файла.

        :param script_path: Путь к файлу-скрипту.
        :param output_func: Функция вывода.
        :param vfs: Объект VFS для передачи в обработчики.
        """
        path = Path(script_path)
        if not path.exists():
            output_func(f"Ошибка: скрипт '{script_path}' не найден")
            return

        with open(path, encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue
                self._execute_line(line, output_func, vfs)

    def _execute_line(self, line: str, output_func, vfs) -> None:
        """Выполняет одну строку скрипта."""
        output_func(f"> {line}")

        command, args = parse_command(line)

        if command == "exit":
            self.logger.log(line)
            return

        handler = COMMANDS.get(command)
        if handler is None:
            error = f"команда '{command}' не найдена"
            output_func(f"Ошибка: {error}")
            self.logger.log(line, error)
            return

        result = handler(vfs, args)
        output_func(result)
        self.logger.log(line)