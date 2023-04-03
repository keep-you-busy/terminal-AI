import psycopg2

from config.config import settings

create_if_not_exist = """CREATE TABLE IF NOT EXISTS MESSAGES (
   chat_id SERIAL PRIMARY KEY,
   role VARCHAR(20),
   content TEXT,
   timestamp TIMESTAMP DEFAULT NOW()
 );"""


insert_to_the_messages = '''INSERT INTO MESSAGES (chat_id, role, content) VALUES (%s, %s, %s)'''

select_max_chat_id = 'SELECT MAX(chat_id) FROM chat_history;'


def get_db_init_connection(db_url, db_request):
    """Initial connection to the database."""
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        crsr = connection.cursor()
        crsr.execute(db_request)
        connection.commit()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated')


def get_chat_id(db_url):
    """Determinate chat id."""
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        crsr = connection.cursor()
        crsr.execute("SELECT MAX(chat_id) FROM chat_history;")
        result = crsr.fetchone()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()
            return result


def make_db_default_values(db_url, script):
    """Taking user's values from config."""
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        crsr = connection.cursor()
        for message in settings.MESSAGES:
            role = message['role']
            content = message['content']
            crsr.execute(script, (role, content))
        connection.commit()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated')


def insert_db_new_values(db_url, script, messages, chat_id):
    """Create history chat."""
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        crsr = connection.cursor()
        for message in messages:
            role = message['role']
            content = message['content']
            crsr.execute(script, (chat_id, role, content))
        connection.commit()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated')

get_db_init_connection(settings.DATABASE_URL, create_if_not_exist)
make_db_default_values(settings.DATABASE_URL, insert_to_the_messages)
