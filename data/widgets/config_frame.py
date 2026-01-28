import tkinter.ttk as ttk


class ConfigFrame(ttk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text='——' ,*args, **kwargs)
        self.content = ttk.Frame(self, takefocus=0)
        self.config_frame = {
            'top': ttk.Frame(self, takefocus=0),
            'bottom': ttk.Frame(self, takefocus=0),
            'left': ttk.Frame(self, takefocus=0),
            'right': ttk.Frame(self, takefocus=0)
        }
        self.config_frame['top'].pack(side='top', anchor='n', fill='x', expand=True)
        self.config_frame['bottom'].pack(side='bottom', anchor='s', fill='x', expand=True)
        self.config_frame['left'].pack(side='left', anchor='w', fill='y', expand=True)
        self.config_frame['right'].pack(side='right', anchor='e', fill='y', expand=True)

        self.content.pack(anchor='center', expand=True, fill='both')