from urllib.parse import quote

from sqlalchemy import create_engine, text

from settings import psql_db, psql_host, psql_password, psql_username


class Postgres:
    def __init__(self):
        self.db = psql_db
        self.host = psql_host
        self.password = psql_password
        self.username = psql_username
        self.engine = None

    def create_connection(self):
        self.engine = create_engine(
            f'postgresql+psycopg2://{self.username}:%s@{self.host}/{self.db}' % quote(f'{self.password}'))

    def get_connection(self):
        if self.engine is None:
            self.create_connection()
        return self.engine

    def truncate(self, schema, table):
        self.execute(f'TRUNCATE table {schema}.{table}')

    def execute(self, query):
        if self.engine is None:
            self.create_connection()
        with self.engine.connect() as con:
            con.execute(text(query))
