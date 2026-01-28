import tkinter.ttk as ttk
from ..global_const import *


class ResistanceInstance(ttk.Frame):
    def __init__(self, master, super_list):
        super().__init__(master, takefocus=0)
        self.master = master
        self.super_list = super_list
        self.label = ttk.Label(self, text='Resistance:')
        self.combobox = ttk.Combobox(self, values=RESIST)
        self.delete_button = ttk.Button(self, text='–', command=self.delete)

        self.label.grid(row=0, column=0)
        self.combobox.grid(row=0, column=1)
        self.delete_button.grid(row=0, column=2, ipadx=5, padx=5)

    def get(self):
        return self.combobox.get()

    def delete(self):
        self.super_list.remove(self)
        self.destroy()
