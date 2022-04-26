from http import HTTPStatus
from fastapi import FastAPI, Depends
from Stats_Service.models import Streak, User, Game, Wins
import sqlite3
import contextlib
import uuid

app = FastAPI()



def get_db():
    with contextlib.closing(sqlite3.connect("StatDB_0.db")) as db:
        db.row_factory = sqlite3.Row
        yield db

# Posting a win or loss for a particular game, along with a timestamp and number of guesses.
@app.post("/games")
def add_game(user: User, game: Game, s: Streak, w: Wins, db: sqlite3.Connection = Depends(get_db)):
    shard_key = user.user_id % 3
    if shard_key == 0:
        db.execute(
            """
            INSERT INTO games (user_id, game_id, finished, guesses, won) VALUES (?, ?, ?, ?, ?);
            """, ([game.user_id], [game.game_id], game.finished, game.guesses, game.won, )
        )
        db.commit()
        
        return HTTPStatus.OK
        
    elif shard_key == 1:
        # db.execute(
        #     """
        #     INSERT INTO wins (user_id, COUNT(won)) VALUES (?, ?);
        #     """, ([w.user_id], [w.wins], )
        # )
        # db.commit()
        
        # return HTTPStatus.OK
        pass
    
    elif shard_key == 2:
        db.execute(
            """
            INSERT INTO streaks (user_id, streak, beginning, ending) VALUES (?, ?, ?, ?);
            """, ([s.user_id], [s.streak], s.finished, s.guesses, )
        )
        db.commit()
        
        return HTTPStatus.OK


# Retrieving the statistics for a user.
@app.get("/games/{user_id}")
def get_statistics(user_id: str, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT game_id, finished, guesses, won FROM games WHERE user_id = (?);
        """, ([user_id]))
    stats = cur.fetchall()
    print(user_id)
    return {"Stats": stats}

# Retrieving the top 10 users by number of wins


@app.get("/top10wins")
def get_top_10_users_by_wins(db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    return {"Top_10_Wins": wins}


# Retrieving the top 10 users by longest streak
@ app.get("/top10streak")
def get_top_10_users_by_longest_streak(db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    streaks = cur.fetchall()
    return {"Top_10_Streaks": streaks}