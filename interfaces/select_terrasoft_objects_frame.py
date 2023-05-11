from tkinter import *
from tkinter import ttk
from ttkwidgets import CheckboxTreeview
import interfaces.mapping_main_frame as mmf
import config


class SelectTerrasoftObjectFrame:

    def __init__(self, backend, root, debug):
        self.backend = backend
        self.root = root
        self.debug = debug

    def get_select_terrasoft_object_frame(self):
        terrasoft_object_frame = ttk.Frame()
        tables = self.backend.get_terrasoft_objects()
        new_tables = {}
        grouped_tables = tables
        tables_to_tree = [{'group_name': x, 'tables': grouped_tables[x]} for x in grouped_tables]
        for i in range(len(tables_to_tree)):
            tables_to_tree[i]['group_id'] = i + 1
            tables_to_tree[i]['tables'] = [
                {'value': x, 'id': str(i + 1) + '_' + str(tables_to_tree[i]['tables'].index(x))} for x in
                tables_to_tree[i]['tables']]
            for table in tables_to_tree[i]['tables']:
                new_tables[table['id']] = table['value']
        tree = CheckboxTreeview(terrasoft_object_frame)
        tree.pack(expand=True,fill=BOTH, anchor=CENTER)
        for group in tables_to_tree:
            tree.insert("", "end", group['group_id'], text='  ' + group['group_name'])
            for table in group['tables']:
                tree.insert(group['group_id'], "end", table['id'], text='  ' + table['value'])
        # next_button = ttk.Button(terrasoft_object_frame, text='Далее', command= lambda: self.get_checked_objects(new_tables))
        next_button = ttk.Button(terrasoft_object_frame, text='Далее',
                                 command=lambda: self.get_checked_objects(next_button, [new_tables[x] for x in tree.get_checked()]))
        next_button.pack()
        terrasoft_object_frame.pack(expand=True,fill=BOTH)
        if self.debug:
            next_button.invoke()

    def get_checked_objects(self, button, tables):
        if self.debug:
            tables = ['Currency', 'CurrencyRate', 'CurrencyRateRight']
        mapping_main_frame = mmf.MappingMainFrame(self.backend, self.root, tables, self.debug)
        button.master.destroy()
        mapping_main_frame.get_mapping_main_frame()
