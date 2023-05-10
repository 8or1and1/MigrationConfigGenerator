from tkinter import *
from tkinter import ttk
import interfaces.connection_frame as cf


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
        button.pack()
        begin_frame.pack(expand=True)
        if self.debug:
            button.invoke()


    def __init__(self, backend, debug):
        self.debug = debug
        self.backend = backend
        self.root = Tk()
        self.root.title("Генератор конфиг-файла миграции")
        self.root.geometry("800x800")
        self.generate_begin_frame()
