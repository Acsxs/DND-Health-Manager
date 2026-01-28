import xml.etree.cElementTree as ET
from glob import glob
from os.path import getmtime
from ..widgets.widgets import *
from tkinter import simpledialog
from functools import partial
from time import perf_counter
from .tab import *

class TabRibbon(ConfigFrame):
    def __init__(self, master, size: tuple, frame, tab_types):
        super().__init__(master, takefocus=0)
        self.scrollable_frame = ScrollableFrame(
            self.content,
            size=size,
            scroll_sides={'x': True, 'y': False, 'pack': 'top'},
            side='right',
            takefocus=0,
        )
        self.scrollable_frame.pack(side='top', expand=True, fill='y')
        self.time_since_save = None
        self.tab_types = tab_types
        self.master = master
        self.size = size
        self.tab_frame = frame
        self.tabs = []
        self.buttons = []
        self.selected_tab = None
        self.add_tab_button = ttk.Button(self.config_frame['right'], text="Add Tab", command=self.add_tab)
        self.delete_selected_button = ttk.Button(self.config_frame['right'], text="Delete Tab", command=self.delete_selected)
        self.save_button = ttk.Button(self.config_frame['right'], text="Save", command=self.save)
        self.load_button = ttk.Button(self.config_frame['right'], text="Load", command=self.load)

        self.save_button.grid(row=0, column=0, sticky='we', ipadx=5)
        self.load_button.grid(row=0, column=1, sticky='we', ipadx=5)
        self.add_tab_button.grid(row=1, column=0, sticky='we', ipadx=5)
        self.delete_selected_button.grid(row=1, column=1, sticky='we', ipadx=5)

        files = glob("saves/*.xml")
        files.sort(key=getmtime)
        if files:
            self.load(files[-1])

    def delete_selected(self):
        if not self.selected_tab:
            return
        self.tabs.remove(self.selected_tab[0])
        self.buttons.remove(self.selected_tab[1])
        self.selected_tab[0].destroy()
        self.selected_tab[1].destroy()
        self.selected_tab = None

    def save(self):
        save_name = simpledialog.askstring(title="Name", prompt="Save name: ")
        if not save_name:
            return
        self.time_since_save = perf_counter()
        tabs = ET.Element("tabs")
        for i in self.tabs:
            i.save(tabs)
        tree = ET.ElementTree(tabs)
        tree.write(f"saves/{save_name}.xml")

    def load(self, name=None):
        if name is None:
            files = glob("saves/*.xml")
            files.sort(key=getmtime)
            files = list(reversed(files))
            files = [i.removeprefix("saves\\").removesuffix(".xml") for i in files]
            popup = DialogCombobox(self, "Save: ", files)
            name = popup.get()
            if name is None:
                return
            name = f"saves\\{name}.xml"
        self.clear()
        self.time_since_save = perf_counter()
        tree = ET.parse(name)
        root = tree.getroot()
        for tabs in root:
            tab, name = self.add_tab(tabs.get('name'), tabs.tag)
            tab.load(tabs)

    def select_tab(self, selected_tab):
        for tab in self.tabs:
            if tab != selected_tab:
                tab.hide()
        selected_tab.show()
        index = self.tabs.index(selected_tab)
        for i, button in enumerate(self.buttons):
            if i != index:
                button.config(state="normal")
                button.state(['!pressed'])
                continue
            button.config(state="disabled")
            button.state(['pressed'])
        self.selected_tab = [selected_tab, self.buttons[index]]

    def add_tab(self, tab_name=None, tab_type=None):
        if tab_name is None:
            tab_name = simpledialog.askstring(title="Name", prompt="Tab name: ")
        if not tab_name:
            return
        if tab_type is None:
            if len(self.tab_types.keys()) == 1:
                tab = list(self.tab_types.values())[0]
            else:
                popup = DialogCombobox(self, "Tab type: ", list(self.tab_types.keys()))
                tab_type_name = popup.show()
                if tab_type_name is None:
                    return
                tab = self.tab_types[tab_type_name]
        else:
            tab = self.tab_types[tab_type]
        tab = tab(self.tab_frame, tab_name)
        button = ttk.Button(self.scrollable_frame.get(), text=tab_name, command=partial(self.select_tab, tab))
        button.state(['!pressed'])
        button.pack(side='left', anchor='w', expand=True, fill='y', ipadx=10)
        self.tabs.append(tab)
        self.buttons.append(button)
        return tab, button

    def clear(self):
        for tab in self.tabs:
            tab.destroy()
        for button in self.buttons:
            button.destroy()
        self.tabs.clear()
        self.buttons.clear()

    # def configure_size(self, width):
    #     rel_width = width - self.config.winfo_width()
    #     # print(rel_width)
    #     self.scrollable_frame.configure_size(width=rel_width)
