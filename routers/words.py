from fastapi import APIRouter

router = APIRouter()


@router.get("/words/validate/{word}")
async def validate_word(word: str):
    if len(word) == 5:
        return {"result": "valid"}
    return {"result": "invalid"}
