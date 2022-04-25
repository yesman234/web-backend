import sqlite3
from fastapi import FastAPI, Depends
from models import User, Game
import contextlib
import uuid

app = FastAPI()

# Posting a win or loss for a particular game, along with a timestamp and number of guesses.


def get_db():
    with contextlib.closing(sqlite3.connect("StatDB_0.db")) as db:
        db.row_factory = sqlite3.Row
        yield db


@app.post("/games")
def add_game(user: User, game: Game):
    shard_key = user.user_id % 3
    if shard_key == 0:
        # INSERT INTO games_shard_0(user_id, game_id, finished, guesses, won)  VALUES(?, ?, ?, ?, ?)
        pass
    elif shard_key == 1:
        # INSERT INTO games_shard_1(user_id, game_id, finished, guesses, won)  VALUES(?, ?, ?, ?, ?)
        pass
    elif shard_key == 2:
        # INSERT INTO games_shard_2(user_id, game_id, finished, guesses, won)  VALUES(?, ?, ?, ?, ?)
        pass


# Retrieving the statistics for a user.
@app.get("/games/{user_id}")
def get_statistics(user_id: int):
    pass

# Retrieving the top 10 users by number of wins


@app.get("/top10wins/{user_id}")
def get_top_10_users_by_wins(db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur
    return {wins}


# Retrieving the top 10 users by longest streak
@ app.get("/top10streak")
def get_top_10_users_by_longest_streak(db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    streaks = cur
    return {streaks}
