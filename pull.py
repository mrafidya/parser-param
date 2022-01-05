import logging
from datetime import datetime
from pathlib import Path
from sys import exit, exc_info

import pandas as pd
from sqlalchemy import text
from Postgres import Postgres
from Sqlite import Sqlite

def get_query():
    with open('get_function.sql') as f:
        return f.read()

def main():
    current_year = datetime.now().year
    logging_path = Path('logs', f'{current_year}.log')
    logging.basicConfig(filename=logging_path,
                        format='%(asctime)s:%(filename)s:%(levelname)s - %(message)s',
                        datefmt='%Y-%b-%d %X%z',
                        level=logging.INFO)

    
        sqlite = Sqlite()
        pg = Postgres()

        logging.info('Get data from production db')
        df = pd.read_sql(sql=text(get_query()), con=pg.get_connection())

        logging.info('Drop function table in local db')
        sqlite.execute('DROP table IF EXISTS functions')

        logging.info('Insert function definition to local db')
        df.to_sql('functions', con=sqlite.get_connection())
        logging.info('pull.py done')


if __name__ == '__main__':
    main()
