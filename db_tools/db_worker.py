import config
from db_tools._terrasoft_db_connector import terrasoftConnector
from db_tools._elma_db_connector import elmaConnector

class db_worker:
    def __init__(self):
        self.terrasoft_worker = terrasoftConnector()
        self.elma_worker = elmaConnector()

    def get_terrasoft_objects(self):
        tables = self.terrasoft_worker.get_table_names()
        filtered_tables = list(filter(lambda item: '1' not in item, list(filter(lambda item: '_' in item, tables))))
        import re
        tables_splitted = [re.sub(r'([A-Z])', r' \1', x.split('_')[1], count=2).split() for x in filtered_tables]
        one_word_tables = [''.join(x) for x in tables_splitted if len(x) == 1]
        grouped_tables = {'Other': []}
        for t in one_word_tables:
            current_group = [''.join(x) for x in tables_splitted if x[0] == t]
            if len(current_group) == 1:
                grouped_tables['Other'].append(t)
            else:
                grouped_tables[t] = current_group

        return grouped_tables