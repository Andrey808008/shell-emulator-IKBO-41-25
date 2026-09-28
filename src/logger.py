"""Логирование команд эмулятора в CSV-файл"""

import csv
from datetime import datetime
from pathlib import Path


class Logger:
    """Пишет события вызова команд в CSV-файл"""

    def __init__(self, log_path: str | None) -> None:

        self.log_path = log_path
        if log_path:
            self._ensure_file()

    def _ensure_file(self) -> None:
        """Создаёт CSV-файл с заголовком, если его ещё нет"""
        path = Path(self.log_path)
        if not path.exists():
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["datetime", "command", "error"])

    def log(self, command: str, error: str = "") -> None:

        if not self.log_path:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, command, error])