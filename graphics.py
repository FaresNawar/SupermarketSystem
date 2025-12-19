"""
This file is responsible for handling the GUI components of the project.
Windows, buttons, labels, frames, etc.
"""

# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)

import tkinter as tk
from tkinter import ttk
import classes

class Frame(ttk.Frame):
    """
    Wrapper for the ttk.Frame class
    """
    def __init__(self, master: tk.Tk | tk.Toplevel, padding: int):
        super().__init__(master=master, padding=padding)


class Label(ttk.Label):
    """
    Wrapper for the ttk.Label class
    """
    def __init__(self, master, text: str, font_size: int):
        super().__init__(master=master, text=text, font=("Arial", font_size))


class SupermarketApplication:
    """
    Where all hell breaks loose
    """
    def __init__(self):
        width, height = 720, 512

        self.screen = tk.Tk()
        self.screen.geometry("%dx%d" % (width, height))
        self.screen.title("My Supermarket System")
        self.screen.resizable(width=False, height=False)

        self.__build__()
        self.screen.focus_set()
        self.screen.mainloop()

    def __build__(self):
        self.cframe = Frame(self.screen, 10)
        self.cframe.place(relx=0.5, rely=0.5, anchor='center')
        Label(self.cframe, "Hello, world!", 15).grid()