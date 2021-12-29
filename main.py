import logging
from datetime import datetime
from pathlib import Path
from sys import argv, exit, exc_info

import pandas as pd

from Postgres import Postgres
from modules import extractor, load_data, load_from_db
from settings import psql_schema, psql_table


def main():
    current_year = datetime.now().year
    logging_path = Path('logs', f'{current_year}.log')
    logging.basicConfig(filename=logging_path,
                        format='%(asctime)s:%(filename)s:%(levelname)s - %(message)s',
                        datefmt='%Y-%b-%d %X%z',
                        level=logging.INFO)
    try:
        logging.debug('Checking argument')
        if len(argv) < 3:
            banner = ''' Example usage: 
                    python main.py file data/function.sql
                    python main.py db data/function.db persist
                '''
            print(banner)
            logging.error('Argument not valid')
            logging.info('Exiting script')
            exit(1)

        logging.debug('Reading source')
        if argv[1] == 'file':
            path = Path(argv[2])
            func_definition = load_data(path)
        elif argv[1] == 'db':
            func_definition = load_from_db(argv[2])
        else:
            logging.error('[source] arguments is not valid')
            logging.info('Exiting script')
            exit(1)

        logging.info('Start parsing..')
        results = extractor(func_definition)
        logging.info('Parser is done, saving the results..')

        new_columns = ['process_name', 'relation', 'table_name']
        df = pd.DataFrame(results, columns=['raw'])
        df[new_columns] = df['raw'].str.split(';', expand=True)

        df.to_csv(
            path_or_buf=Path('output', 'text.csv'),
            columns=new_columns,
            sep=';',
            index=False,
            header=False)

        logging.info('Results successfully saved to csv file')

        if len(argv) > 3 and argv[3] == 'persist':
            logging.info('"persist" argument is set, saving the results to database')

            pg = Postgres()
            pg.truncate(psql_schema, psql_table)
            df = df[['process_name', 'relation', 'table_name']]
            df.to_sql(
                con=pg.get_connection(),
                schema=psql_schema,
                name=psql_table,
                if_exists='append',
                index=False)

            logging.info(f'Results successfully saved {psql_schema}.{psql_table}')

        logging.info(f'Done, number of results: {df.shape[0]}')
    except:
        logging.error('Exception occurred!')
        logging.error(f'Exception captured:{exc_info()[0]}')
        exit(1)


if __name__ == '__main__':
    main()
