from http import HTTPStatus
from fastapi import FastAPI, Depends
from Stats_Service.models import User, Game
import sqlite3
import contextlib
import uuid

app = FastAPI()



def get_db():
    with contextlib.closing(sqlite3.connect("StatDB_0.db")) as db:
        db.row_factory = sqlite3.Row
        yield db
def get_db1():
    with contextlib.closing(sqlite3.connect("StatDB_1.db")) as db1:
        db1.row_factory = sqlite3.Row
        yield db1
def get_db2():
    with contextlib.closing(sqlite3.connect("StatDB_2.db")) as db2:
        db2.row_factory = sqlite3.Row
        yield db2

# Posting a win or loss for a particular game, along with a timestamp and number of guesses.
@app.post("/games")
def add_game(game: Game, db: sqlite3.Connection = Depends(get_db), 
             db1: sqlite3.Connection = Depends(get_db1), db2: sqlite3.Connection = Depends(get_db2)):
    shard_key = int(uuid.UUID(game.user_id)) % (3)
    print(shard_key)
    if shard_key == 0:
        print(shard_key)
        print(type(game.user_id))
        print(game.user_id)
        db.execute(
            """
            INSERT INTO games (user_id, game_id, finished, guesses, won) VALUES (?, ?, ?, ?, ?);
            """, (game.user_id, game.game_id, game.finished, game.guesses, game.won, )
        )
        db.commit()
        
        return HTTPStatus.OK
        
    elif shard_key == 1:
        db1.execute(
            """
            INSERT INTO games (user_id, game_id, finished, guesses, won) VALUES (?, ?, ?, ?, ?);
            """, ([game.user_id], [game.game_id], game.finished, game.guesses, game.won, )
        )
        db1.commit()
        
        return HTTPStatus.OK
    
    elif shard_key == 2:
        db2.execute(
            """
            INSERT INTO games (user_id, game_id, finished, guesses, won) VALUES (?, ?, ?, ?, ?);
            """, ([game.user_id], [game.game_id], game.finished, game.guesses, game.won, )
        )
        db2.commit()
        
        return HTTPStatus.OK


# Retrieving the statistics for a user.
@app.get("/games/{user_id}")
def get_statistics(user_id: str, db: sqlite3.Connection = Depends(get_db)):
    shard_key = user_id.format(3)
    if shard_key == 0:
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