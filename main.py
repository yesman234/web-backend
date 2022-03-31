from fastapi import FastAPI
from routers import words

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(words.router)
