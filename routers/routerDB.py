import sqlite3
import json
import ast

connection = sqlite3.connect('routers.db')
mycursor = connection.cursor()

with open('answers.json') as f:
    data = json.load(f)

data = ast.literal_eval(json.dumps(data))

dataList = [data]

mycursor.execute(
    "CREATE TABLE IF NOT EXISTS answers(words text)")

#mycursor.executemany("INSERT INTO answers(words) VALUES (?)", (dataList))

print("Command executed sucesssfully...")
connection.commit()


connection.close()
