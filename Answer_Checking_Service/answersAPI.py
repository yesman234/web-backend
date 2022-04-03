from fastapi import FastAPI

app = FastAPI()

# Checking a valid guess against the answer for the current day
@app.post("/answers/{word}")
def check_guess_against_answer(word: str):
    pass

# Changing the answers for future games
@app.put("/answers")
def change_answer():
    pass
