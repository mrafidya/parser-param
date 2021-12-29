from sqlalchemy import create_engine


def load_data(path):
    with open(path, 'r') as file:
        return file.read()


def load_from_db(db):
    engine = create_engine(f'sqlite:///{db}')
    function_list = engine.execute('select routine_definition from functions') \
        .fetchall()
    return '\n'.join(f[0] for f in function_list)
