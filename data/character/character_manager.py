from .character import *


class CharacterManager(ConfigFrame):
    def __init__(self, master, size, update_targets):
        super().__init__(master, takefocus=0)
        self.scrollable_frame = ScrollableFrame(
            self.content,
            size=size,
            scroll_sides={'x': False, 'y': True, 'pack': 'right'},
            takefocus=0
        )
        self.characters = []
        self.heal_all_button = ttk.Button(self.config_frame['bottom'], text='Heal All', command=self.heal_all)
        self.add_instance_button = ttk.Button(self.config_frame['bottom'], text='Add character', command=self.add_character)
        self.show_tmh_checkbutton = ttk.Checkbutton(self.config_frame['bottom'], text='Show true max health', command=lambda: self.show_tmh(self.show_tmh_checkbutton.state()))
        self.show_tmh_checkbutton.state(['!selected'])
        self.update_targets = update_targets

        self.scrollable_frame.grid(row=0, column=0)

        self.heal_all_button.pack(side='left', anchor='s')
        self.add_instance_button.pack(side='left', anchor='s')
        self.show_tmh_checkbutton.pack(side='left', anchor='s')

    def heal_all(self):
        for character in self.characters:
            character.heal()

    def add_character(self, chara_name=''):
        character = Character(self.scrollable_frame.get(), self.update_targets, self.remove_character, chara_name)
        character.pack(side='top', fill='x')
        if self.characters:
            character.health.health.set(self.characters[-1].health.health.get())
            character.health.max_health.set(self.characters[-1].health.max_health.get())
            character.health.true_max_health.set(self.characters[-1].health.true_max_health.get())
            character.health.update_health_bar()
        self.characters.append(character)
        return character

    def remove_character(self, character):
        self.characters.remove(character)
        character.destroy()
        self.update_targets()

    def get(self, name):
        for character in self.characters:
            if name == character.name.get():
                return character

    def show_tmh(self, state):
        state = True if "selected" in state else False
        for character in self.characters:
            character.health.show_hide_tmh(state)
