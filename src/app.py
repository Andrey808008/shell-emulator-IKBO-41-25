"""Графическое приложение эмулятора командной оболочки."""

import argparse
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

from src.commands import COMMANDS
from src.logger import Logger
from src.parser import parse_command
from src.script_runner import ScriptRunner
from src.vfs import Vfs


class ShellApp:
    """GUI-приложение — эмулятор командной оболочки."""

    def __init__(self, root: tk.Tk, args: argparse.Namespace) -> None:
        """Инициализирует окно, VFS и виджеты."""
        self.root = root
        self.args = args

        self.logger = Logger(args.log)
        self.script_runner = ScriptRunner(self.logger)

        self.vfs = Vfs()
        if args.vfs:
            try:
                self.vfs.load_zip(args.vfs)
            except Exception as exc:
                self._vfs_error = str(exc)
            else:
                self._vfs_error = None
        else:
            self._vfs_error = None

        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED, height=25
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.entry.bind("<Return>", self.on_enter)

        self.entry.focus_set()

        self.print_output("Добро пожаловать в эмулятор командной оболочки.")
        self.print_output("Введите команду и нажмите Enter. Для выхода: exit\n")

    def print_output(self, text: str) -> None:
        """Печатает строку в область вывода."""
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_enter(self, event: tk.Event) -> None:
        """Обрабатывает нажатие Enter в поле ввода."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        self.print_output(f"> {line}")

        if not line.strip():
            return

        command, args = parse_command(line)

        if command == "exit":
            self.logger.log(line)
            self.root.destroy()
            return

        handler = COMMANDS.get(command)
        if handler is None:
            error = f"команда '{command}' не найдена"
            self.print_output(f"Ошибка: {error}")
            self.logger.log(line, error)
            return

        result = handler(self.vfs, args)
        self.print_output(result)
        self.logger.log(line)