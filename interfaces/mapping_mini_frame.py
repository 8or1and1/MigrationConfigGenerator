from tkinter import *
from tkinter import ttk
import config
import shelve


class MappingMiniFrame:

    def __init__(self, backend, table_name, elma_params, debug=False):
        self.elma_columns = None
        self.backend = backend
        self.debug = debug
        self.table_name = table_name
        self.elma_params = elma_params
        self.terrasoft_columns = self.backend.terrasoft_worker.get_column_names(self.table_name)

    def get_mapping_mini_frame(self):
        window = Tk()
        window.title(self.table_name + ' -> ' + self.elma_params['namespace'] + '.' + self.elma_params['code'])
        window.geometry("500x500")
        picked_elma_columns = []
        row = 0
        self.elma_columns = self.backend.elma_worker.get_columns(self.elma_params['namespace'],self.elma_params['code'])
        elma_column_codes = [x['code'] for x in self.elma_columns]
        elma_column_codes.append('')
        for column_name in self.terrasoft_columns:
            label = ttk.Label(window, text=column_name)
            label.grid(row=row, column=0)
            picked_elma_columns.append(StringVar(value=elma_column_codes[0]))
            combobox = ttk.Combobox(window, values=elma_column_codes, textvariable=picked_elma_columns[row])
            combobox.grid(row=row, column=1)
            en = ttk.Entry(window)
            en.grid(row=row, column=2)
            row += 1

        btn = ttk.Button(window, text='Собрать конфиг', command=lambda: self.click(window))
        btn.grid(row=row, column=0, columnspan=2)

    def click(self, window):
        preconfig_values = {'columns':{}}
        for i in range(int((len(window.children)-1)/3)):
            name_addition = '' if i == 0 else str(i+1)
            label_name = '!label{}'.format(name_addition)
            combobox_name = '!combobox{}'.format(name_addition)
            entry_name = '!entry{}'.format(name_addition)
            elma_re = window.children[entry_name].get()
            terrasoft_column_name = window.children[label_name]['text']
            elma_column_name = window.children[combobox_name].get()
            if terrasoft_column_name and elma_column_name:
                preconfig_values['columns'][terrasoft_column_name] = {'name':elma_column_name, 're':''}
            if elma_re:
                preconfig_values['columns'][terrasoft_column_name]['re'] = elma_re

        if preconfig_values['columns'] == {}:
            return
        preconfig_values['namespace'] = self.elma_params['namespace']
        preconfig_values['code'] = self.elma_params['code']
        print(11)
        with shelve.open(config.SHELVE_NAME) as config_shelve:
            config_shelve[self.table_name] = preconfig_values
        window.destroy()
