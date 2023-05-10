from tkinter import *
from tkinter import ttk
from interfaces.mapping_mini_frame import MappingMiniFrame
import config


class MappingMainFrame:

    def __init__(self, backend, root, terrasoft_objects, debug=False):
        self.backend = backend
        self.root = root
        self.terrasoft_objects = terrasoft_objects
        self.debug = debug
        self.mapped_objects = []

    def get_mapping_main_frame(self):
        mapping_main_frame = ttk.Frame()
        for x in self.terrasoft_objects:
            button = ttk.Button(mapping_main_frame, text=x, command=lambda: self.click(button, x))
            button.pack(anchor=CENTER, expand=1)
        mapping_main_frame.pack(expand=True, fill=BOTH)

    def click(self, button, object_name):
        style = ttk.Style()
        style.configure('Green.TButton', foreground='green')
        button.configure(style='Green.TButton', text=object_name, command=None)
        mmf = MappingMiniFrame(self.backend, self.debug)
