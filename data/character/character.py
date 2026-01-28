from .health import *


class Character(ttk.LabelFrame):
    def __init__(self, master, update_targets, super_delete, name='', *args, **kwargs):
        super().__init__(master, text='——', *args, **kwargs, takefocus=0)
        self.master = master
        self.name = tk.StringVar()
        self.name.set(name)

        self.super_delete = super_delete
        self.update_targets = update_targets

        self.label = LabelWidgetPair(self, "Name: ", CustomEntry(self, textvariable=self.name))
        self.label.widget.bind('<KeyRelease>', lambda e: self.update_targets())

        self.config_frame = ttk.Frame(self, takefocus=0)

        self.delete_button = ttk.Button(self.config_frame, text='Delete', command=lambda: self.super_delete(self))
        self.heal_button = ttk.Button(self.config_frame, text='Heal', command=self.heal)
        self.health = Health(self)

        self.label.grid(row=0, column=0)
        self.health.grid(row=1, column=0, columnspan=3)
        self.delete_button.pack(side='right')
        self.heal_button.pack(side='right')
        self.config_frame.grid(row=0, column=2)
        self.columnconfigure(1, weight=1)

    def apply_damage(self, damage):
        self.health.apply_damage(damage)

    def heal(self):
        self.health.health.set(self.health.max_health.get())
        self.health.update_health_bar()
