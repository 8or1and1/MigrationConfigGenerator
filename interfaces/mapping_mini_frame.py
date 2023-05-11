from tkinter import *
from tkinter import ttk


class MappingMiniFrame:

    def __init__(self, backend, table_name, elma_params, debug=False):
        self.backend = backend
        self.debug = debug
        self.table_name = table_name
        self.elma_params = elma_params
        self.terrasoft_columns = self.backend.terrasoft_worker.get_column_names(self.table_name)

    def get_mapping_mini_frame(self):
        window = Tk()
        window.title(self.table_name + ' -> ' + self.elma_params['namespace'] + '.' + self.elma_params['code'])
        window.geometry("500x500")
        row = 0
        for column_name in self.terrasoft_columns:
            label = ttk.Label(window, text=column_name)
            label.grid(row=row, column=0)
            row += 1

    def click(self, parent_frame):
        window = Tk()
        window.title("Новое окно")
        window.geometry("500x500")
