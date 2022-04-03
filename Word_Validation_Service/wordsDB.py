import json
import sqlite3

answers = open('answers.json')
words = json.load(answers)
words = [(x,) for x in words]
db_name = "wordDB"


db = sqlite3.connect(db_name)
cursor = db.cursor()

# Create tables
cursor.execute(
    '''
    DROP TABLE IF EXISTS dailyWord
    '''
)
cursor.execute(
    '''
    DROP TABLE IF EXISTS gameGuesses
    '''
)
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS dailyWord( id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)
    '''
)
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS gameGuesses( id INTEGER PRIMARY KEY AUTOINCREMENT, guesses TEXT[])
    '''
)

query = '''INSERT INTO dailyWord (word) VALUES (?);'''
cursor.executemany(query, words)
db.commit()
print(cursor.rowcount)
db.close()
