import json
from tkinter import *
from tkinter import ttk
from interfaces.mapping_mini_frame import MappingMiniFrame
import config
import shelve


class MappingMainFrame:

    def __init__(self, backend, root, terrasoft_objects, debug=False):
        self.backend = backend
        self.root = root
        self.terrasoft_objects = terrasoft_objects
        self.debug = debug
        self.mapped_objects = []
        self.elma_full_apps = self.backend.elma_worker.get_apps()

    def get_mapping_main_frame(self):
        mapping_main_frame = ttk.Frame()
        elma_apps = [x['code'] for x in self.elma_full_apps]
        row = 0
        picked_elma_apps = []
        for x in self.terrasoft_objects:
            label = ttk.Label(mapping_main_frame, text=x)
            label.grid(row=row, column=0)
            picked_elma_apps.append(StringVar(value=elma_apps[0]))
            combobox = ttk.Combobox(mapping_main_frame, values=elma_apps, textvariable=picked_elma_apps[row])
            combobox.grid(row=row, column=1)
            button = ttk.Button(mapping_main_frame, text=x)
            button['command'] = lambda button=button, x=x, row=row: self.click(button, x, row)
            button.grid(row=row, column=2)
            row += 1
        generate_button = ttk.Button(mapping_main_frame, text='Собрать конфиг', command=self.generate)
        generate_button.grid(row=row, column=0, columnspan=3)
        mapping_main_frame.pack(expand=True, fill=BOTH)

    def get_elma_app_parameters_by_name(self, app_code):
        for x in self.elma_full_apps:
            if x['code'] == app_code:
                return x

    def click(self, button, object_name, row):
        style = ttk.Style()
        style.configure('Green.TButton', foreground='green')
        button.configure(style='Green.TButton', text=object_name, command=None)
        elma_params = self.get_elma_app_parameters_by_name(
            button.master.children['!combobox' + ('' if row == 0 else str(row+1))].get())
        mmf = MappingMiniFrame(self.backend, object_name, elma_params, self.debug)
        mmf.get_mapping_mini_frame()

    def generate(self):
        config_dict = {}
        with shelve.open(config.SHELVE_NAME) as config_shelve:
            for key in config_shelve.keys():
                config_dict[key] = config_shelve[key]
        config_json = json.dumps(config_dict)
        with open('config.json', 'w') as outfile:
            outfile.write(config_json)
        print(config_json)
