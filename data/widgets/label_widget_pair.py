import tkinter.ttk as ttk


class LabelWidgetPair(ttk.Frame):
    def __init__(self, master, text, widget, *args, **kwargs):
        super().__init__(master, takefocus=0, *args, **kwargs)
        self.label = ttk.Label(self, text=text)
        self.widget = widget

        self.label.grid(row=0, column=0)
        self.widget.grid(row=0, column=1)
