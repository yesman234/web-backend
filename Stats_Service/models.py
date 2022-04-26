from pydantic import BaseModel
from datetime import datetime


class Game(BaseModel):
    user_id: int
    game_id: int
    finished: datetime
    guesses: int
    won: bool


class User(BaseModel):
    user_id: int
    username: str
    
    
class Streak(BaseModel):
    user_id: int
    streak: int
    beginning: datetime
    end: datetime


class Wins(BaseModel):
    user_id: int
    won: int