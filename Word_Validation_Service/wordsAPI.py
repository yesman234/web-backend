from fastapi import FastAPI, Depends
from pydantic import BaseModel
import contextlib
import sqlite3
from typing import List

app = FastAPI()

WORDLE_WORD_LENGTH = 5

class Guess(BaseModel):
    word: str

def get_db():
    with contextlib.closing(sqlite3.connect("WordValidationDB")) as db:
        db.row_factory = sqlite3.Row
        yield db

@app.post("/WordValidations")
def validate_word(guess: Guess,  db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT word FROM gameDictionary WHERE word = (?);
        """
        , (guess.word, )
    )
    word_found = cur.fetchall()

    return { "word_valid": True } if word_found else { "word_valid": False }
