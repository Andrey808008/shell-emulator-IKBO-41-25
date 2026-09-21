import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext


#Парсер команды
def parse_command(line: str) -> tuple[str, list[str]]:
    parts = line.strip().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


#Обработчики команд
def handle_ls(args: list[str]) -> str:
    return f"Выполнена команда: ls, аргументы: {args}"

def handle_cd(args: list[str]) -> str:
    return f"Выполнена команда: cd, аргументы: {args}"


#Приложение
class ShellApp:
    COMMANDS = {
        "ls": handle_ls,
        "cd": handle_cd,
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        #заголовок
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
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_enter(self, event: tk.Event) -> None:
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        self.print_output(f"> {line}")

        if not line.strip():
            return

        command, args = parse_command(line)

        if command == "exit":
            self.root.destroy()
            return

        handler = self.COMMANDS.get(command)
        if handler is None:
            self.print_output(f"Ошибка: команда '{command}' не найдена")
            return

        result = handler(args)
        self.print_output(result)


def main() -> None:
    root = tk.Tk()
    ShellApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()