from tkinter import *
from tkinter import ttk


class MappingMiniFrame:

    def __init__(self, backend, table_name, debug=False):
        self.backend = backend
        self.debug = debug
        self.table_name = table_name


    def get_mapping_mini_frame(self):
        mapping_mini_frame = ttk.Frame()
        button = ttk.Button(mapping_mini_frame,text="Создать окно", command=lambda: self.click(self))
        button.pack( anchor=CENTER, expand=1)
        mapping_mini_frame.pack(expand=True,fill=BOTH)

    def click(self, parent_frame):
        window = Tk()
        window.title("Новое окно")
        window.geometry("500x500")

