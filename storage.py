import sqlite3
import datetime

class Storage:
    create_msg_q = ('create table if not exists '
                    'message('
                        'text text not null, '
                        'date integer not null, '
                        'chat_id integer not null, '
                        'date_digested integer, '
                        'id integer primary key autoincrement) ')

    create_url_q  = ('create table if not exists '
                     'url('
                         'url text not null, '
                         'date integer not null, '
                         'chat_id integer not null, '
                         'date_downloaded integer, '
                         'id integer primary key autoincrement) ')

    insert_msg_q = ('insert into message values '
                    '(?, ?, ?, null, null) ')

    insert_url_q = ('insert into url values '
                    '(?, ?, ?, null, null) ')

    select_new_msg_q = ('select * from message '
                        'where chat_id = ? '
                        'and date_digested is null ')

    select_new_url_q = ('select * from url '
                        'where date_downloaded is null ')

    update_msg_q = ('update message '
                    'set date_digested = ? '
                    'where chat_id = ? '
                    'and date_digested is null ')

    update_url_q = ('update url '
                    'set date_downloaded = ? '
                    'where url = ? ')

    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(Storage.create_msg_q)
        self.cursor.execute(Storage.create_url_q)
        self.connection.commit()

    def store_message(self, msg):
        self.cursor.execute(Storage.insert_msg_q,
                            [msg['text'], msg['date'], msg['chat']['id'] ])
        self.connection.commit()

    def store_url(self, msg):
        self.cursor.execute(Storage.insert_url_q,
                            [msg['text'], msg['date'], msg['chat']['id'] ])
        self.connection.commit()

    def digest(self, chat_id, classifier):
        now = datetime.datetime.utcnow()
        unix_time = int((now - datetime.datetime(1970, 1, 1)).total_seconds())
        self.cursor.execute(Storage.select_new_msg_q, [ chat_id ])
        classes = {}
        for row in self.cursor:
            text = row[0]
            classes.setdefault(classifier.classify(text), []).append(text) # Append; create if the class is empty.
        self.cursor.execute(Storage.update_msg_q, [ unix_time , chat_id ]) # Mark the messages as digested in the DB.
        self.connection.commit()
        return classes

    def get_urls(self):
        self.cursor.execute(Storage.select_new_url_q)
        urls = []
        for row in self.cursor:
            url = row[0]
            urls.append(url)
        return urls

    def mark_downloaded(self, url):
        now = datetime.datetime.utcnow()
        unix_time = int((now - datetime.datetime(1970, 1, 1)).total_seconds())
        self.cursor.execute(Storage.update_url_q, [unix_time, url])
        self.connection.commit()

    def finalize(self):
        self.cursor.close()
        self.connection.close()
