import json
import sqlite3
import os


# 5 letter dictionary words from https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
file = open('sgb-words.txt', 'r')
valid_words = file.readlines()
file.close()
words = [(word.strip(),) for word in valid_words]


db = sqlite3.connect("WordValidationDB")
cursor = db.cursor()
cursor.execute(
    '''DROP TABLE IF EXISTS gameDictionary;''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS gameDictionary ( id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT);''')
query = '''INSERT INTO gameDictionary (word) VALUES (?);'''
cursor.executemany(query, words)
db.commit()
print(cursor.rowcount)
db.close()
