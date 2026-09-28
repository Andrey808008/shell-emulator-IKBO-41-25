"""Выполнение стартового скрипта с командами эмулятора"""

from pathlib import Path

from src.commands import COMMANDS
from src.logger import Logger
from src.parser import parse_command


class ScriptRunner:
    """Выполняет команды из файла-скрипта"""

    def __init__(self, logger: Logger) -> None:

        self.logger = logger

    def run(self, script_path: str, output_func) -> None:
        path = Path(script_path)
        if not path.exists():
            output_func(f"Ошибка: скрипт '{script_path}' не найден")
            return

        with open(path, encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue
                self._execute_line(line, output_func)

    def _execute_line(self, line: str, output_func) -> None:
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

        result = handler(args)
        output_func(result)
        self.logger.log(line)