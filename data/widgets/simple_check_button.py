import tkinter.ttk as ttk
import tkinter as tk


class SimpleCheckButton(ttk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        self.variable = tk.IntVar()
        super().__init__(master, variable=self.variable, *args, **kwargs)

    def get(self):
        return bool(self.variable.get())

    def set(self, state):
        self.variable.set(int(state))
