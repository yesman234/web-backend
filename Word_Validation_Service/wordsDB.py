import json
import sqlite3

answers = open('answers.json')
words = json.load(answers)
words = [(x,) for x in words]


db = sqlite3.connect("db")
cursor = db.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS dailyWord( id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)''')
query = '''INSERT INTO answers (word) VALUES (?);'''
cursor.executemany(query, words)
db.commit()
print(cursor.rowcount)
db.close()
