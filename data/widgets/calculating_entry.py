from ..global_const import *
import tkinter.ttk as ttk
import tkinter as tk
from re import fullmatch
from sympy import simplify


class CustomEntry(ttk.Entry):
    def __init__(self, master, *args, **kwargs):
        self.value = tk.StringVar()
        if 'textvariable' not in kwargs:
            kwargs['textvariable'] = self.value
        super().__init__(master, *args, **kwargs)
        self.separator = ttk.Separator(master, orient="horizontal")
        self.separator.place(in_=self, x=0, rely=1.0, height=2, relwidth=1.0)

    def get(self):
        return self.value.get()

    def set(self, string):
        self.value.set(string)


def math_expr_validate(value):
    if value == "":
        return True
    if fullmatch(MATH_EXPRESSION_REGEX, value) is None:
        return False
    return True


class CalculatingEntry(CustomEntry):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.set('0')
        self.bind("<Return>", lambda e: self.update())
        self.bind("<FocusOut>", lambda e: self.update())
        self.bind("<FocusIn>", lambda e: self.update())

    def update(self):
        string = self.get()
        if not math_expr_validate(string) or string == "":
            return
        result = simplify(string)
        result = f"{float(result)}".split('.')
        result = result[0] + '.' + result[1].rstrip('0') if result[1] != '0' else result[0]
        self.set(result)
