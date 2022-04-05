from . import decorators

import sqlite3


@decorators.singleton
class AnswersDB:
    def __init__(self):
        print('Loading Answer Database')
        self.connection = sqlite3.connect('database/answers.db') 
        self.cursor = self.connection.cursor()

        # populate table
        self.cursor.execute('''DROP TABLE IF EXISTS answers''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers (answer TEXT,
                                                                   date TIMESTAMP)''')
        self.connection.commit()

    def __repr__(self):
        records = self.cursor.execute('''SELECT rowid, * FROM answers''').fetchall()
        records = ['\n'.join(record) for record in recods]
        return records + '\n'

    def __del__(self):
        self.connection.close()

    def create():
        print('...')
        self.connection.commit()

    def read():
        print('...')

    def update():
        print('...')
        self.connection.commit()

    def delete():
        print('...')
        self.connection.commit()

