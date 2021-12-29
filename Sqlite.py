from sqlalchemy import create_engine, text

from settings import sqlite_db


class Sqlite:
    def __init__(self):
        self.db = sqlite_db
        self.engine = None

    def create_connection(self):
        self.engine = create_engine(f'sqlite:///{self.db}')

    def get_connection(self):
        if self.engine is None:
            self.create_connection()
        return self.engine

    def execute(self, query):
        if self.engine is None:
            self.create_connection()
        with self.engine.connect() as con:
            con.execute(text(query))
