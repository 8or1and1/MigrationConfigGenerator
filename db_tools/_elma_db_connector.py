import psycopg2
from psycopg2.extras import NamedTupleCursor


class elmaConnector:
    def __init__(self):
        self.connection = None

    def connect(self, config):
        try:
            self.connection = psycopg2.connect(dbname=config['database'],
                                               user=config['user'],
                                               # user='pidoras',
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
        records_smaller = []
        with self.connection.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT fields FROM head.appviews")
            records = cur.fetchall()
            for record in records:
                record_small = {'code': record.code, 'namespace': record.namespace,
                                'name': record.name}  # , 'fields':record.fields }
                records_smaller.append(record_small)
        return records_smaller

