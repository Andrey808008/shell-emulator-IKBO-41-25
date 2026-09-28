"""Точка входа в приложение"""

import tkinter as tk

from src.app import ShellApp
from src.config import parse_arguments


def main() -> None:
    """Запускает приложение"""
    args = parse_arguments()

    root = tk.Tk()
    app = ShellApp(root, args)

    app.print_output("Параметры запуска")
    app.print_output(f"VFS:    {args.vfs}")
    app.print_output(f"LOG:    {args.log}")
    app.print_output(f"SCRIPT: {args.script}")
    app.print_output("==================")

    root.mainloop()


if __name__ == "__main__":
    main()