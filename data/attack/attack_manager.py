from .attack_instance import *


class AttackManager(ConfigFrame):
    def __init__(self, master, size, apply_damage):
        super().__init__(master, takefocus=0)
        self.scrollable_frame = ScrollableFrame(
            self.content,
            size=size,
            scroll_sides={'x': False, 'y': True, 'pack': 'right'},
            takefocus=0,
        )
        self.super_apply_damage = apply_damage
        self.attack_instances = []
        self.targets = []
        self.target_frame = ttk.Frame(self.config_frame['top'], takefocus=0)
        self.target_label = ttk.Label(self.target_frame, text="Select Target")
        self.target_combobox = ttk.Combobox(self.target_frame, values=self.targets)
        self.apply_damage_button = ttk.Button(self.config_frame['bottom'], text="Apply Damage", command=lambda: self.super_apply_damage(self.get(), self.target_combobox.get()))
        self.add_instance_button = ttk.Button(self.config_frame['bottom'], text="Add Attack", command=self.add_attack_instance)
        self.clear_button = ttk.Button(self.config_frame['bottom'], text="Clear", command=self.clear_instances)

        self.scrollable_frame.grid(row=0, column=0, sticky='we')

        self.target_frame.pack(side='top', anchor='n')
        self.target_label.grid(row=0, column=0)
        self.target_combobox.grid(row=0, column=1)

        self.apply_damage_button.pack(side='left', anchor='w')
        self.clear_button.pack(side='left', anchor='w')
        self.add_instance_button.pack(side='right', anchor='e')

    def add_attack_instance(self):
        attack_instance = AttackInstance(self.scrollable_frame.get(), self.super_apply_damage, self.attack_instances, self.targets)
        self.attack_instances.append(attack_instance)
        attack_instance.pack(side='top')
        return attack_instance

    def get(self):
        new_damage = DamageCollector()
        for i in self.attack_instances:
            new_damage += i.get()
        return new_damage

    def clear_instances(self):
        for i in self.attack_instances:
            damage_instances = i.damage_instances
            for j in damage_instances:
                j.damage_entry.set(0)

    def update_targets(self, targets):
        current_index = self.target_combobox.current()
        self.targets = targets
        self.target_combobox.config(values=self.targets)
        if current_index == -1:
            self.target_combobox.set('')
        else:
            self.target_combobox.current(current_index)

        for attack in self.attack_instances:
            current_index = attack.target.current()
            attack.target.config(values=self.targets)
            if current_index == -1:
                attack.target.set('')
                continue
            attack.target.current(current_index)

