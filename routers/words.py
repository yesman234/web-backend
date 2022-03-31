from fastapi import APIRouter

router = APIRouter()

@router.get("/words/validate/{word}")
def validate_word(word: str):
    if word is "hello":
        return {"result": "valid"}
    return {"result": "invalid"}
