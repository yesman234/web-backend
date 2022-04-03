import contextlib
import sqlite3
from typing import List
from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()

WORDLE_WORD_LENGTH = 5

class Guess(BaseModel):
    guess_word: str
    game_id: str

def get_db():
    with contextlib.closing(sqlite3.connect("wordDB")) as db:
        db.row_factory = sqlite3.Row
        yield db

@app.post("/WordValidations")
async def validate_guess(
    guess: Guess, db: sqlite3.Connection = Depends(get_db)):
    if guess.game_id == "":
        query =(
            """
            INSERT INTO gameGuesses (guesses) VALUES(?);
            """
        )
        await db.execute(query, [guess.guess_word])
        return { "result_valid": True }
        

    prev_guesses: List[str] = await db.execute(
        """
        SELECT guesses FROM gameGuesses WHERE id = {guess.game_id};
        """
    )

    if guess.guess_word in prev_guesses or len(guess.guess_word) != WORDLE_WORD_LENGTH:
        return { "result_valid": False }
    
    prev_guesses.append(guess.guess_word)

    await db.execute(
        """
        UPDATE gameGuesses SET guesses = {prev_guesses} WHERE id = {guess.game_id};
        """
    )
    
    return { "result_valid": True }

@app.get("/words/validate/{word}")
async def validate_word(word: str):
    if len(word) == WORDLE_WORD_LENGTH:
        return {"result_valid": True}
    return {"result_valid": False}
