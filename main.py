from tkinter.messagebox import askyesnocancel

from data.attack.attack_manager import *
from data.character.character_manager import *
from data.notebook.tab_ribbon import *
from data.resistance.resistance_manager import *


# move tabs
class CharacterType(Tab):
    def __init__(self, master, name):
        super().__init__(master, name, takefocus=0)
        self.character_manager = CharacterManager(self, (310, 350), self.update_targets)
        self.attack_manager = AttackManager(self, (300, 350), self.apply_damage)
        self.resistance_manager = ResistanceManager(self, (300, 350))
        # self.web_page = WebFrame(self, 100, width=875, height=100, highlightthickness=1, highlightbackground='red')

        self.character_manager.grid(row=0, column=0, padx=2)
        self.attack_manager.grid(row=0, column=1, padx=2)
        self.resistance_manager.grid(row=0, column=2, padx=2)

        # self.web_page.grid(row=0, column=3, columnspan=3)
        # self.character_manager.add_character('ad')

    def apply_damage(self, damage_collector, target):
        target = self.character_manager.get(target)
        resistances = self.resistance_manager.get_resistances()
        for k, v in damage_collector.items():
            damage_type, magical = damage_type_deconvert(k)
            target.apply_damage(calculate_resistances(damage_type, magical, resistances) * v)

    def update_targets(self):
        targets = [character.name.get() for character in self.character_manager.characters]
        self.attack_manager.update_targets(targets)

    def save(self, element):
        data = ET.SubElement(element, "character_type", name=self.name)

        character_manager = ET.SubElement(data, "character_manager")
        characters = ET.SubElement(character_manager, "characters")
        for character in self.character_manager.characters:
            character_elem = ET.SubElement(characters, "character", name=f"{character.name.get()}")
            ET.SubElement(character_elem, "health").text = character.health.health.get()
            ET.SubElement(character_elem, "max_health").text = character.health.max_health.get()
            ET.SubElement(character_elem, "true_max_health").text = character.health.true_max_health.get()
        ET.SubElement(character_manager, "show_tmh").text = f"{True if 'selected' in self.character_manager.show_tmh_checkbutton.state() else False}"

        attack_manager = ET.SubElement(data, "attack")
        attacks = ET.SubElement(attack_manager, "attacks")
        for index, attack in enumerate(self.attack_manager.attack_instances):
            attack_elem = ET.SubElement(attacks, f"attack{index}")

            damage_modifier = attack.damage_modifier.get()
            damage_modifier_elem = ET.SubElement(attack_elem, "damage_modifier")
            ET.SubElement(damage_modifier_elem, "type").text = f"{damage_modifier[0]}" if damage_modifier[0] else ''
            ET.SubElement(damage_modifier_elem, "damage").text = f"{damage_modifier[1]}"
            ET.SubElement(damage_modifier_elem, "magical").text = f"{damage_modifier[2]}"

            damage_instance_1 = attack.damage_instance_1.get()
            damage_instance_1_elem = ET.SubElement(attack_elem, "damage_instance_1")
            ET.SubElement(damage_instance_1_elem, "type").text = f"{damage_instance_1[0]}" if damage_instance_1[0] else ''
            ET.SubElement(damage_instance_1_elem, "damage").text = f"{damage_instance_1[1]}"
            ET.SubElement(damage_instance_1_elem, "magical").text = f"{damage_instance_1[2]}"

            damage_instance_2 = attack.damage_instance_2.get()
            damage_instance_2_elem = ET.SubElement(attack_elem, "damage_instance_2")
            ET.SubElement(damage_instance_2_elem, "type").text = f"{damage_instance_2[0]}" if damage_instance_2[0] else ''
            ET.SubElement(damage_instance_2_elem, "damage").text = f"{damage_instance_2[1]}"
            ET.SubElement(damage_instance_2_elem, "magical").text = f"{damage_instance_2[2]}"

            ET.SubElement(attack_elem, "current_target").text = attack.target.get()

        targets_elem = ET.SubElement(attack_manager, "targets")
        for index, target in enumerate(self.attack_manager.targets):
            ET.SubElement(targets_elem, f"target{index}").text = target

        ET.SubElement(attack_manager, "current_target").text = self.attack_manager.target_combobox.get()

        resistance_manager = ET.SubElement(data, "resistance_manager")
        for index, resistance in enumerate(self.resistance_manager.get_resistances()):
            ET.SubElement(resistance_manager, f"resistance{index}").text = resistance

    def load(self, tree):
        character_manager, attack_manager, resistance_manager = tree

        characters, show_tmh = character_manager
        show_tmh = int(show_tmh.text == 'True')
        self.character_manager.show_tmh_checkbutton.state(["!" * (1 - show_tmh) + "selected", '!alternate'])
        if len(characters):
            for character_attributes in characters:
                character = self.character_manager.add_character(character_attributes.get('name'))
                character.health.health.set(character_attributes.find('health').text)
                character.health.max_health.set(character_attributes.find('max_health').text)
                character.health.true_max_health.set(character_attributes.find('true_max_health').text)

        attacks, targets,  current_target = attack_manager

        if len(targets):
            self.attack_manager.targets = [target.text for target in targets]
            self.attack_manager.update_targets(self.attack_manager.targets)

        if current_target.text in self.attack_manager.targets:
            self.attack_manager.target_combobox.current(self.attack_manager.targets.index(current_target.text))
        else:
            self.attack_manager.target_combobox.set(current_target.text)

        if len(attacks):
            for attack_attributes in attacks:
                attack = self.attack_manager.add_attack_instance()
                damage_instances = {i.tag: i for i in attack_attributes}

                damage_modifier = damage_instances['damage_modifier']
                damage_type = damage_modifier.find('type').text
                damage_type = damage_type if damage_type in ALL else ''
                magical = damage_modifier.find('magical').text == 'True'
                attack.damage_modifier.combobox.set(damage_type)
                attack.damage_modifier.damage_entry.set(damage_modifier.find('damage').text)
                attack.damage_modifier.checkbox.set(magical)
                attack.damage_modifier.check_type()

                damage_instance_1 = damage_instances['damage_instance_1']
                damage_type = damage_instance_1.find('type').text
                damage_type = damage_type if damage_type in ALL else ''
                magical = damage_instance_1.find('magical').text == 'True'
                attack.damage_instance_1.combobox.set(damage_type)
                attack.damage_instance_1.damage_entry.set(damage_instance_1.find('damage').text)
                attack.damage_instance_1.checkbox.set(magical)
                attack.damage_instance_1.check_type()

                damage_instance_2 = damage_instances['damage_instance_2']
                damage_type = damage_instance_2.find('type').text
                damage_type = damage_type if damage_type in ALL else ''
                magical = damage_instance_2.find('magical').text == 'True'
                attack.damage_instance_2.combobox.set(damage_type)
                attack.damage_instance_2.damage_entry.set(damage_instance_2.find('damage').text)
                attack.damage_instance_2.checkbox.set(magical)
                attack.damage_instance_2.check_type()

                target = attack_attributes.find('current_target').text
                if target in self.attack_manager.targets:
                    attack.target.current(self.attack_manager.targets.index(target))
                else:
                    attack.target.set(target)

        if len(resistance_manager):
            for resistance_attributes in resistance_manager:
                resistance = self.resistance_manager.add_resistance()
                resistance_type = resistance_attributes.text
                resistance_type = resistance_type if resistance_type in RESIST else ''
                resistance.combobox.set(resistance_type)


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0)
        self.master = master
        self.tab_frame = ttk.Frame(self, width=1000, height=750)
        self.tab_ribbon = TabRibbon(self, (1000 - 170, 50), self.tab_frame, {"character_type": CharacterType})

        self.tab_ribbon.grid(row=0, column=0)
        self.tab_frame.grid(row=1, column=0)


def on_closing():
    global app
    if app.tab_ribbon.time_since_save is not None:
        if app.tab_ribbon.time_since_save - perf_counter() < 60:
            root.destroy()
            return
    answer = askyesnocancel("Quit", "Do you want to save?")
    if answer is None:
        return
    if answer:
        app.tab_ribbon.save()
    root.destroy()
    return


def escape(event):
    root.focus_set()


root = tk.Tk()
style = ttk.Style(root)

root.title("D&D Manager")
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "dark")
root.iconbitmap("data/icon/dnd.ico")
root.geometry("1025x550")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Escape>", escape)


app = App(root)

root.mainloop()
