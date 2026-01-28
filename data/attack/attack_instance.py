from .damage_instance import *
from .damage_collector import *


class AttackInstance(ConfigFrame):
    def __init__(self, master, apply_damage, super_list, targets, *args, **kwargs):
        super().__init__(master, takefocus=0, *args, **kwargs)
        self.master = master
        self.damage_modifier = DamageInstance(self.content)
        self.damage_instance_1 = DamageInstance(self.content)
        self.damage_instance_2 = DamageInstance(self.content)
        self.super_list = super_list
        self.super_apply_damage = apply_damage

        self.bottom_config = self.config_frame['bottom']
        self.target = ttk.Combobox(self.bottom_config, values=targets, width=5)
        self.apply_damage_button = ttk.Button(self.bottom_config, text="Apply", command=lambda: self.super_apply_damage(self.get(), self.target.get()))
        self.delete_self_button = ttk.Button(self.bottom_config, text="–", command=self.remove_self)
        self.save_success_checkbutton = SimpleCheckButton(self.bottom_config, text="Sav Success?")

        self.damage_modifier.pack(side='top', anchor='n', expand=True, fill='x')
        self.damage_instance_1.pack(side='left', anchor='s', expand=True)
        self.damage_instance_2.pack(side='left', anchor='s', expand=True)

        self.apply_damage_button.pack(side='left', anchor='w')
        self.save_success_checkbutton.pack(side='left', anchor='w')
        self.delete_self_button.pack(side='right', anchor='e', ipadx=5)
        self.target.pack(side='right', anchor='e')

    def get(self):
        damage = DamageCollector()

        damage.add(self.damage_modifier.get())
        damage.add(self.damage_instance_1.get())
        damage.add(self.damage_instance_2.get())

        damage = damage / 2 if self.save_success_checkbutton.get() else damage
        self.save_success_checkbutton.set(False)
        return damage

    def remove_self(self):
        self.super_list.remove(self)
        self.destroy()
