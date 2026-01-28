from ..widgets.widgets import *
from math import ceil


class Health(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.health = CalculatingEntry(self, width=3, justify='center')
        self.max_health = CalculatingEntry(self, width=3, justify='center')
        self.true_max_health = CalculatingEntry(self, width=3, justify='center')

        self.health.set('10')
        self.max_health.set('10')
        self.true_max_health.set('10')

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=193, mode='determinate')
        self.progress_bar['value'] = int(self.health.get() or self.max_health.get() or 0)

        self.seperator_label = ttk.Label(self, text='/')
        self.opening_parenthesis_label = ttk.Label(self, text='(')
        self.closing_parenthesis_label = ttk.Label(self, text=')')
        self.percentage_label = ttk.Label(self, text='100%')

        self.health.bind("<KeyRelease>", lambda e: self.update_health_bar())
        self.max_health.bind("<KeyRelease>", lambda e: self.update_health_bar())
        self.true_max_health.bind("<KeyRelease>", lambda e: self.update_health_bar())

        self.progress_bar.grid(row=0, column=0)
        self.health.grid(row=0, column=1)
        self.seperator_label.grid(row=0, column=2)
        self.max_health.grid(row=0, column=3)
        self.percentage_label.grid(row=0, column=7)

        self.update_health_bar()

    def apply_damage(self, damage):
        health = float(self.health.get())
        damage = float(ceil(damage))
        current_health = ceil(health - damage)
        self.health.set(f"{current_health}")
        self.update_health_bar()

    def update_health_bar(self):
        health = float(self.health.get() or 10)
        max_health = float(self.max_health.get() or 10)
        percent = int(100 * health / max_health)
        self.progress_bar['value'] = percent
        # print(self.progress_bar['value'])
        self.percentage_label['text'] = f'{percent}%'

    def get(self):
        return self.health.get()

    def show_hide_tmh(self, state):
        if state:
            self.progress_bar.configure(length=141)
            self.opening_parenthesis_label.grid(row=0, column=4)
            self.true_max_health.grid(row=0, column=5)
            self.closing_parenthesis_label.grid(row=0, column=6)
            return
        self.progress_bar.configure(length=190)
        self.opening_parenthesis_label.grid_forget()
        self.true_max_health.grid_forget()
        self.closing_parenthesis_label.grid_forget()
