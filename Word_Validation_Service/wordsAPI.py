from fastapi import FastAPI

app = FastAPI()

WORDLE_WORD_LENGTH = 5

@app.get("/words/validate/{word}")
async def validate_word(word: str):
    if len(word) == WORDLE_WORD_LENGTH:
        return {"result_valid": True}
    return {"result_valid": False}
