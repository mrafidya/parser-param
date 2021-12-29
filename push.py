import logging
from datetime import datetime
from pathlib import Path
from sys import exit, exc_info

import pandas as pd
from neo4j import GraphDatabase

from settings import neo4j_driver, neo4j_host, neo4j_password, neo4j_username


def create_driver(uri, username, password):
    return GraphDatabase.driver(uri, auth=(username, password))


def close_driver(driver):
    driver.close()


def clean_db(session):
    session.run('MATCH (n:Function) DETACH DELETE n')
    session.run('MATCH (n:Table) DETACH DELETE n')


def load_source(*args, **kwargs):
    return pd.read_csv(*args, **kwargs)


def prepare_data(dataFrame):
    dataFrame['rel'] = dataFrame['rel'].str.replace('source', 'hasSource')
    dataFrame['rel'] = dataFrame['rel'].str.replace('target', 'hasTarget')
    return dataFrame


def create_rel(relationship):
    return '''
        MERGE (f:Function {name: $function})
        MERGE (t:Table {name: $target})
        MERGE (f)-[:%s]->(t)
    ''' % relationship


def create_node(session, df):
    for _, row in df.iterrows():
        query = create_rel(row['rel'])
        session.run(query, function=row['function'], target=row['target'])


def drop_index(session):
    session.run('DROP INDEX function_name IF EXISTS')
    session.run('DROP INDEX table_name IF EXISTS')


def create_index(session):
    session.run(
        'CREATE INDEX function_name IF NOT EXISTS FOR (n:Function) ON (n.name)')
    session.run(
        'CREATE INDEX table_name IF NOT EXISTS FOR (n:Table) ON (n.name)')


def main():
    current_year = datetime.now().year
    logging_path = Path('logs', f'{current_year}.log')
    logging.basicConfig(filename=logging_path,
                        format='%(asctime)s:%(filename)s:%(levelname)s - %(message)s',
                        datefmt='%Y-%b-%d %X%z',
                        level=logging.INFO)
    try:
        logging.info('Create neo4j connection')
        uri = f'{neo4j_driver}://{neo4j_host}:7687'
        username = neo4j_username
        password = neo4j_password
        driver = create_driver(uri, username, password)

        logging.info('Load source from ./output/text.csv')
        col_names = ['function', 'rel', 'target']
        df = load_source(
            Path('output', 'text.csv'),
            sep=';', header=None, names=col_names)
        df = prepare_data(df)

        logging.info('Start inserting data...')
        with driver.session() as session:
            logging.debug('Drop index')
            drop_index(session)
            logging.debug('Clean existing data')
            clean_db(session)
            logging.debug('Insert data')
            create_node(session, df)
            logging.debug('Recreate index')
            create_index(session)

        close_driver(driver)
        logging.info('push.py done')
    except:
        logging.error('Exception occurred!')
        logging.error(f'Exception captured:{exc_info()[0]}')
        exit(1)



if __name__ == '__main__':
    main()
