from ..widgets.widgets import *
from .resistance_instance import *


def calculate_resistances(damage_type, magical, resistances):
    calc = lambda e: (1 / 2 if e in resistances else (1 / 2 if damage_type in resistances else 1))
    return calc('magical') if magical else calc('non-magical')


class ResistanceManager(ConfigFrame):
    def __init__(self, master, size):
        super().__init__(master, takefocus=0)
        self.scrollable_frame = ScrollableFrame(
            self.content,
            size=size,
            scroll_sides={'x': False, 'y': True, 'pack': 'right'},
            takefocus=0,
        )
        self.resistance_instances = []
        self.add_instance_button = ttk.Button(self.config_frame['bottom'], text='Add resistance', command=self.add_resistance)

        self.scrollable_frame.grid(row=0, column=0)

        self.add_instance_button.pack(side='bottom', anchor='s')

    def add_resistance(self):
        resistance = ResistanceInstance(self.scrollable_frame.get(), self.resistance_instances)
        resistance.pack(side='top')
        self.resistance_instances.append(resistance)
        return resistance

    def get_resistances(self):
        resistances = []
        for i in self.resistance_instances:
            resistances.append(i.get())
        resistances = list(set(resistances))
        return resistances
