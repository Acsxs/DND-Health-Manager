import tkinter.ttk as ttk
import tkinter as tk


class DialogCombobox(tk.Toplevel):
    def __init__(self, parent, text, values):
        super().__init__(parent)
        self.title("Select save")
        self.label = ttk.Label(self, text=text)
        self.label.grid(row=0, column=0)

        self.combobox = ttk.Combobox(self, width=20, values=values)
        self.combobox.grid(row=0, column=1, columnspan=3)

        self.ok_button = ttk.Button(self, text="OK", command=self.select)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.cancel)
        self.ok_button.grid(row=1, column=2, pady=10)
        self.cancel_button.grid(row=1, column=3, pady=10)

        self.selection = None

    def select(self):
        selection = self.combobox.get()
        if selection:
            self.selection = selection
        self.destroy()

    def cancel(self):
        self.selection = None
        self.destroy()

    def show(self):
        self.deiconify()
        self.wm_protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window(self)
        return self.selection

    def get(self):
        result = self.show()
        return result
