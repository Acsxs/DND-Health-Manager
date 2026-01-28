import tkinter.ttk as ttk
import tkinter as tk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container: tk.Widget, size, scroll_sides, side="top", *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.pointer_inside = False
        self.scroll_sides = scroll_sides
        self.size = list(size)
        self.canvas = tk.Canvas(self, width=size[0], height=size[1], takefocus=0)
        self.configure_canvas = lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if scroll_sides['x'] and scroll_sides['y']:
            self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
            self.scrollbar_y.pack(side=scroll_sides['pack'][0], fill="y")
            self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.pack(side=scroll_sides['pack'][1], fill="x")
            self.default = True
        elif scroll_sides['y']:
            self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
            self.scrollbar_y.pack(side=scroll_sides['pack'], fill="y")
            self.default = True

        elif scroll_sides['x']:
            self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.pack(side=scroll_sides['pack'], fill="x")
            self.default = False

        self.scrollable_frame = ttk.Frame(self.canvas, height=size[0], width=size[1], takefocus=0)
        self.scrollable_frame.bind("<Configure>", self.configure_canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side=side, fill="both", expand=True)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.bind("<Enter>", self.pointer_enter)
        self.bind("<Leave>", self.pointer_leave)

    def get(self):
        return self.scrollable_frame

    def on_mousewheel(self, event):
        if not self.pointer_inside:
            return
        units = -int(event.delta / 120)
        alternate_scroll = int(event.state) == 12
        x_scroll = (self.scroll_sides['x']) and (self.canvas.xview() != (0, 1.0)) and (alternate_scroll == self.default)
        y_scroll = (self.scroll_sides['y']) and (self.canvas.yview() != (0, 1.0)) and (alternate_scroll != self.default)

        if x_scroll:
            self.canvas.xview_scroll(units, "units")
            return
        if y_scroll:
            self.canvas.yview_scroll(units, "units")

    def configure_size(self, width=None, height=None):
        if width and height:
            self.configure(width=width, height=height)
            self.scrollable_frame.configure(width=width, height=height)
            self.canvas.configure(width=width, height=height)
            self.size = [width, height]
            return
        if width:
            self.configure(width=width, height=self.size[1])
            self.scrollable_frame.configure(width=width, height=self.size[1])
            self.canvas.configure(width=width, height=self.size[1])
            self.size[0] = width
            return
        if height:
            self.configure(width=self.size[0], height=height)
            self.scrollable_frame.configure(width=self.size[0], height=height)
            self.canvas.configure(width=self.size[0], height=height)
            self.size[1] = height
            return

    def pointer_enter(self, event):
        self.scrollable_frame.bind_all('<MouseWheel>', self.on_mousewheel)
        self.pointer_inside = True

    def pointer_leave(self, event):
        self.pointer_inside = False


class ScrollableGridFrame(ttk.Frame):
    def __init__(self, container, size, scroll_sides=None, *args, **kwargs):
        # Sides is which sides the scrollbar should appear from
        super().__init__(container, *args, **kwargs)  # Initialises the frame
        self.canvas = tk.Canvas(self, height=size[0], width=size[1])
        self.canvas.grid(row=1 - scroll_sides['pack'][0], column=1 - scroll_sides['pack'][1], sticky="news")
        self.scroll_sides = scroll_sides

        if scroll_sides['y']:
            self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.grid(row=1 - scroll_sides['pack'][0], column=scroll_sides['pack'][1], sticky='ns')
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        if scroll_sides['x']:
            self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.grid(row=scroll_sides['pack'][0], column=1 - scroll_sides['pack'][1], sticky='ew')
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame)
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        # Creates a window for the frame in the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if int(event.state) == 4:
            if self.scroll_sides['x']:
                self.canvas.xview_scroll(int(event.delta / 120), "units")
                return
        if self.scroll_sides['y']:
            self.canvas.yview_scroll(int(event.delta / 120), "units")
