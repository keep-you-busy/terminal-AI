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


def get_scripts_from_file(script_file):
    """Get SQL script from the location."""
    try:
        fd = open(script_file, 'r')
        script = fd.read()
        fd.close()
        return script
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f'Error connection to the script file: {error}'
        )


def get_db_init_connection(script, messages=None):
    """Initial connection to the database."""
    connection = None
    try:
        connection = psycopg2.connect(settings.DATABASE_URL)
        crsr = connection.cursor()
        if messages is None:
            crsr.execute(script)
        else:
            crsr.execute(
                script,
                [(message['role'], message['content']) for message in messages]
            )
        connection.commit()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()


def get_chat_id() -> int:
    """Determinate chat id."""
    connection = None
    try:
        connection = psycopg2.connect(settings.DATABASE_URL)
        crsr = connection.cursor()
        crsr.execute("SELECT MAX(chat_id) FROM messages;")
        result = crsr.fetchone()
        if result[0] is None:
            return 1
        return result[0]
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise psycopg2.DatabaseError(
            f'Error connection to the database: {error}'
            )
    finally:
        if connection is not None:
            connection.close()


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


print(get_chat_id())