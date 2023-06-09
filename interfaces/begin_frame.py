from tkinter import *
from tkinter import ttk
import interfaces.connection_frame as cf
from config import SHELVE_NAME
import shelve


class BeginFrame:

    def on_begin_frame_destroy(self, begin_frame):
        begin_frame.destroy()
        connection_frame = cf.ConnectionFrame(self.backend, self.root, self.debug)
        connection_frame.get_connection_frame()

    def generate_begin_frame(self):
        begin_frame = ttk.Frame()
        label = ttk.Label(begin_frame, text="Добро пожаловать в генератор конфига, приятного аппетита!")
        label.pack()
        button = ttk.Button(begin_frame, text='Поехали!', command=lambda: self.on_begin_frame_destroy(begin_frame))
        button2 = ttk.Button(begin_frame, text='Очистить конфиг', command=self.on_clear_config_button_pressed)
        button.pack()
        button2.pack()
        begin_frame.pack(expand=True)
        if self.debug:
            button.invoke()

    def on_clear_config_button_pressed(self):
        with shelve.open(SHELVE_NAME) as config_shelve:
            config_shelve.clear()
        open('config.json', 'w').close()

    def __init__(self, backend, debug):
        self.debug = debug
        self.backend = backend
        self.root = Tk()
        self.root.title("Генератор конфиг-файла миграции")
        self.root.geometry("800x800")
        self.generate_begin_frame()
