#!/usr/bin/python
import sqlite3

class Storage:
    create_query = '''create table if not exists message(text text not null,
                                                         date int not null,
                                                         chat_id int not null,
                                                         date_digested int,
                                                         id integer primary key)'''
    insert_query = '''insert into message values (?, ?, ?, null, null)'''
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

    def finalize(self):
        self.cursor.close()
        self.connection.close()
