import psycopg2
from datetime import datetime
import json

_connection = None
_cursor = None

def get_connection():
    global _connection

    if not _connection:
        # Open a DB connection
        with open('db_config.json','r') as fh:
            config = json.load(fh)

        _connection = psycopg2.connect(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'])
    return _connection

def get_cursor():
    global _cursor
    if not _cursor:
        # Open a database cursor
        _cursor = get_connection().cursor();
    return _cursor

def close_connection():
    global _connection
    global _cursor
    get_connection().close()
    _connection = None
    _cursor = None   


def do_insert(m_id, created_at, app, url, base_url, lang, favourites, username, bot, tags, words, mastodon_text):


    sql_stmt = '''
        INSERT INTO mastodon_schema.mastodon_toots
        (m_id, created_at, app, url, base_url, language, favourites, username, bot, tags, words, mastodon_text)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );    
    '''


    data_row = (m_id, created_at, app, url, base_url, lang, favourites, username, bot, tags, words, mastodon_text)
    get_cursor().execute(sql_stmt, data_row)

    get_connection().commit()



def do_insert_value_dict(value_dict):
    # value_dict = {  'language': 'en', 'favourites': 0, 'username': 'bob', 'bot': False, 'tags': 0, 'characters': 50, 'words': 12}

    do_insert(value_dict['m_id'], datetime.now(), value_dict['app'], value_dict['url'], value_dict['base_url'], value_dict['language'], value_dict['favourites'], value_dict['username'], value_dict['bot'], value_dict['tags'], value_dict['words'], value_dict['mastodon_text'])



def main():
    # example test producer
    # m_id, created_at, app, url, base_url, "language", favourites, username, bot, tags, words, mastodon_text
    # do_insert(12345, datetime.now(), 'app', 'url', 'base_url', 'language', 0, 'username', False, 0, 0, 'mastodon_text')

    value_dict = { 
            'm_id': 4567,
            'app': 'app',
            'url': 'status.url',
            'base_url': 'base_url',  
            'language': 'm_lang', 
            'favourites': 123, 
            'username': 'm_user', 
            'bot': False, 
            'tags': 1, 
            'characters': 2, 
            'words': 3, 
            'mastodon_text': 'm_text'
        }
    do_insert_value_dict(value_dict)

    close_connection()


if __name__ == '__main__':
    main()
