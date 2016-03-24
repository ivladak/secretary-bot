import sqlite3
import datetime

class Storage:
    create_query = '''create table if not exists message(text text not null,
                                                         date int not null,
                                                         chat_id int not null,
                                                         date_digested int,
                                                         id integer primary key)'''
    insert_query = '''insert into message values (?, ?, ?, null, null)'''
    select_new_query = '''select * from message where chat_id = ? and date_digested is null'''
    digest_query = '''update message set date_digested = ? where chat_id = ? and date_digested is null'''
    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(Storage.create_query)
        self.connection.commit()

    def store_message(self, msg):
       self.cursor.execute(Storage.insert_query, [ msg['text'], msg['date'], msg['chat']['id'] ])
       self.connection.commit()

    def digest(self, chat_id, classifier):
        now = datetime.datetime.utcnow()
        unix_time = int((now - datetime.datetime(1970, 1, 1)).total_seconds())
        self.cursor.execute(Storage.select_new_query, [ chat_id ])
        classes = {}
        for row in self.cursor:
            text = row[0]
            classes.setdefault(classifier.classify(text), []).append(text) # Append; create if the class is empty.
        self.cursor.execute(Storage.digest_query, [ unix_time , chat_id ]) # Mark the messages as digested in the DB.
        self.connection.commit()
        return classes

    def finalize(self):
        self.cursor.close()
        self.connection.close()
