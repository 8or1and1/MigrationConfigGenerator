import pandas as pd
import pymssql
import config


class terrasoftConnector:
    def __init__(self):
        self.connection = None

    def connect(self, config):
        try:
            self.connection = pymssql.connect(server=config['server'],
                                              user=config['user'],
                                              password=config['password'],
                                              database=config['database'])
        except:
            pass

    def select_query(self, query, columns= None):
        data = None
        with self.connection.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            data = pd.DataFrame(data) if columns is None else pd.DataFrame(data, columns=columns)
        return data

    def get_table_names(self):
        query = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_TYPE = 'BASE TABLE' order by TABLE_NAME;"
        columns_dataframe = self.select_query(query)
        y = [row[0] for index, row in columns_dataframe.iterrows()]
        return y
