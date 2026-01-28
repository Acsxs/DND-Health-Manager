from ..widgets.widgets import *


class DamageInstance(ConfigFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, takefocus=0, *args, **kwargs)

        self.damage_entry = CalculatingEntry(self.content, width=4, justify='center', font=('Calibri', 14))

        self.new_frame = ttk.Frame(self.config_frame['bottom'])

        self.combobox = ttk.Combobox(self.new_frame, values=ALL, width=13, font=('Calibri', 8), justify='center')
        self.combobox.bind("<<ComboboxSelected>>", lambda e: self.check_type())
        self.combobox.bind("<Return>", lambda e: self.check_type())
        self.combobox.bind("<FocusOut>", lambda e: self.check_type())

        self.checkbox = SimpleCheckButton(self.new_frame)
        self.magical_tooltip = CreateToolTip(self.checkbox, "Magical?")

        self.damage_entry.pack(side='top', anchor='n', expand=True, fill='x', padx=10, pady=10)

        self.combobox.pack(side='left')
        self.checkbox.pack(side='left')

        self.new_frame.pack(side='top', anchor='n')

        self.check_type()

    def check_type(self):
        if (self.combobox.get() in MAGICAL) or (self.combobox.get() == ''):
            self.checkbox_hide()
            self.checkbox.set(True)
            self.combobox.config(width=18)
        else:
            self.checkbox_show()
            self.combobox.config(width=13)
            # self.checkbox.state(['!selected', '!alternate'])

    def checkbox_show(self):
        self.checkbox.pack(side='left')

    def checkbox_hide(self):
        self.checkbox.pack_forget()

    def get(self):
        return [self.combobox.get(), float(self.damage_entry.get()), self.checkbox.get()]