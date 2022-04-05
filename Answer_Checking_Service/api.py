from fastapi import FastAPI
from database import WordsDB, AnswersDB

app = FastAPI()

answers_db = AnswersDB()
words_db = WordsDB()

# print out the words in the DB
print(words_db)

# Checking a valid guess against the answer for the current day
@app.post("/answers/{word}")
def check_guess_against_answer(word: str):
    pass

# Changing the answers for future games
@app.put("/answers")
def change_answer():
    pass
