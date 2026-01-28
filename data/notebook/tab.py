import tkinter.ttk as ttk


class Tab(ttk.Frame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.name = name

    def hide(self):
        self.grid_forget()

    def show(self, row=0, column=0):
        self.grid(row=row, column=column)

    def save(self, element):
        return

    def load(self, tree):
        return

    def configure_size(self, width, height):
        return


