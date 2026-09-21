"""вход в приложение"""
import tkinter as tk

from src.app import ShellApp


def main() -> None:
    root = tk.Tk()
    ShellApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()