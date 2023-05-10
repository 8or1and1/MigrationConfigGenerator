from tkinter import *
from tkinter import ttk
import config
import interfaces.select_terrasoft_objects_frame as stof


class ConnectionFrame:

    def get_connection_frame(self):
        connection_frame = ttk.Frame()
        connection_frame.columnconfigure(index=0, weight=1)
        for c in range(5): connection_frame.rowconfigure(index=c, weight=1)
        label = ttk.Label(connection_frame, text="Проверьте или измените настройки подключения к серверам")
        label.grid(row=0,column=0)
        terrasoft_frame = self.get_terrasoft_frame(connection_frame)
        terrasoft_frame.grid(row=1,column=0)
        elma_frame = self.get_elma_frame(connection_frame)
        elma_frame.grid(row=2, column=0)

        incorrect_label = ttk.Label(connection_frame)
        incorrect_label.grid(row=3, column=0)

        proceed_button = ttk.Button(connection_frame, text='Далее', command=lambda: self.proceed(proceed_button, incorrect_label))
        proceed_button.grid(row=4,column=0)
        connection_frame.pack(expand=True, fill=BOTH)

        if self.debug:
            proceed_button.invoke()

    def proceed(self, button: ttk.Button, label: ttk.Label):
        if self.backend.terrasoft_worker.connection and self.backend.elma_worker.connection:
            button.master.destroy()
            terrasoft_object_frame = stof.SelectTerrasoftObjectFrame(self.backend, self.root, self.debug)
            terrasoft_object_frame.get_select_terrasoft_object_frame()
        else:
            text = 'Elma365' * (not self.backend.elma_worker.connection) + \
                   ', ' * (
                               not self.backend.elma_worker.connection and not self.backend.terrasoft_worker.connection) + \
                   'Terrasoft' * (not self.backend.terrasoft_worker.connection) + ' : проверьте подключение'
            label['text'] = text

    def get_terrasoft_frame(self, parent):
        self.terrasoft_config = {key:StringVar(value=value) for (key, value) in config.terrasoft_config.items()}
        terrasoft_frame = ttk.Frame(parent, borderwidth=2, relief=SOLID)
        label = ttk.Label(terrasoft_frame, text='Terrasoft 3x')
        label.pack(anchor=NW)

        terrasoft_data_frame = ttk.Frame(terrasoft_frame)

        servername_label = ttk.Label(terrasoft_data_frame, text='Server name')
        servername_label.grid(row=0, column=0)

        servername_entry = ttk.Entry(terrasoft_data_frame, textvariable=self.terrasoft_config['server'])
        servername_entry.grid(row=0, column=1)

        username_label = ttk.Label(terrasoft_data_frame, text='Username')
        username_label.grid(row=1, column=0)

        username_entry = ttk.Entry(terrasoft_data_frame, textvariable=self.terrasoft_config['user'])
        username_entry.grid(row=1, column=1)

        password_label = ttk.Label(terrasoft_data_frame, text='Password')
        password_label.grid(row=2, column=0)

        password_entry = ttk.Entry(terrasoft_data_frame, textvariable=self.terrasoft_config['password'])
        password_entry.grid(row=2, column=1)

        dbname_label = ttk.Label(terrasoft_data_frame, text='DB name')
        dbname_label.grid(row=3, column=0)

        dbname_entry = ttk.Entry(terrasoft_data_frame, textvariable=self.terrasoft_config['database'])
        dbname_entry.grid(row=3, column=1)
        terrasoft_data_frame.pack()


        terrasoft_test_connection_button = ttk.Button(terrasoft_frame,
                                                      text='Проверить соединение',
                                                      command=lambda: self.test_connection(
                                                          terrasoft_test_connection_button,
                                                          self.backend.terrasoft_worker,
                                                          {key:value.get() for (key,value) in self.terrasoft_config.items()}))
        terrasoft_test_connection_button.pack()
        if self.debug:
            terrasoft_test_connection_button.invoke()

        return terrasoft_frame


    def get_elma_frame(self, parent):
        self.elma_config = {key:StringVar(value=value) for (key, value) in config.elma_config.items()}
        elma_frame = ttk.Frame(parent, borderwidth=2, relief=SOLID)

        label = ttk.Label(elma_frame, text='elma 3x')
        label.pack(anchor=NW)

        elma_data_frame = ttk.Frame(elma_frame)

        servername_label = ttk.Label(elma_data_frame, text='Server name')
        servername_label.grid(row=0, column=0)

        servername_entry = ttk.Entry(elma_data_frame, textvariable=self.elma_config['server'])
        servername_entry.grid(row=0, column=1)

        port_label = ttk.Label(elma_data_frame, text='Port')
        port_label.grid(row=1, column=0)

        port_entry = ttk.Entry(elma_data_frame, textvariable=self.elma_config['port'])
        port_entry.grid(row=1, column=1)

        username_label = ttk.Label(elma_data_frame, text='Username')
        username_label.grid(row=2, column=0)

        username_entry = ttk.Entry(elma_data_frame, textvariable=self.elma_config['user'])
        username_entry.grid(row=2, column=1)

        password_label = ttk.Label(elma_data_frame, text='Password')
        password_label.grid(row=3, column=0)

        password_entry = ttk.Entry(elma_data_frame, textvariable=self.elma_config['password'])
        password_entry.grid(row=3, column=1)

        dbname_label = ttk.Label(elma_data_frame, text='DB name')
        dbname_label.grid(row=4, column=0)

        dbname_entry = ttk.Entry(elma_data_frame, textvariable=self.elma_config['database'])
        dbname_entry.grid(row=4, column=1)
        elma_data_frame.pack()

        elma_test_connection_button = ttk.Button(elma_frame,
                                                 text='Проверить соединение',
                                                 command=lambda: self.test_connection(
                                                     elma_test_connection_button,
                                                     self.backend.elma_worker,
                                                     {key:value.get() for (key,value) in self.elma_config.items()}))
        elma_test_connection_button.pack()
        if self.debug:
            elma_test_connection_button.invoke()
        return elma_frame


    def test_connection(self, button, worker, worker_config):
        worker.connect(worker_config)
        if worker.connection:
            style = ttk.Style()
            style.configure('Green.TButton', foreground='green')
            button.configure(style='Green.TButton', text='Соединение установлено', command=None)
            for item in [x for x in button.master.children['!frame'].children.values() if isinstance(x, ttk.Entry)]:
                item.config(state=DISABLED)

        else:
            style = ttk.Style()
            style.configure('Red.TButton', foreground='red')
            button.configure(style='Red.TButton', text='Соединение не установлено')

    def __init__(self, backend, root, debug = False):
        self.debug = debug
        self.terrasoft_config = None
        self.elma_config = None
        self.backend = backend
        self.root = root
