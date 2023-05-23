import psycopg2
from psycopg2.extras import NamedTupleCursor


class elmaConnector:
    def __init__(self):
        self.connection = None

    def connect(self, config):
        try:
            self.connection = psycopg2.connect(dbname=config['database'],
                                               user=config['user'],
                                               password=config['password'],
                                               host=config['server'],
                                               port=config['port'])
        except:
            pass

    def get_apps(self):
        records_smaller = []
        with self.connection.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT code, namespace, name, fields FROM head.appviews")
            records = cur.fetchall()
            for record in records:
                record_small = {'code': record.code, 'namespace': record.namespace,
                                'name': record.name}
                records_smaller.append(record_small)
        return records_smaller

    def get_columns(self, namespace, code):
        useful_system_columns = ['__name', '__id', '__createdAt', '__updatedAt']
        with self.connection.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                'SELECT fields FROM head.appviews where namespace=\'{}\' and code=\'{}\''.format(namespace, code))
            records = cur.fetchall()

            columns = [{'code': x['code'], 'type': x['type'], 'single': x['single']} for x in records[0].fields if
                       x['code'] in useful_system_columns or '__' not in x['code']]

        return columns
