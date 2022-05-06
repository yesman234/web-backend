from fastapi import Depends
import sqlite3
import contextlib
import redis

redisClient = redis.StrictRedis(host="localhost", port=6379, db=0)

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

def updateTop10Wins(db: sqlite3.Connection = Depends(get_db), db1: sqlite3.Connection = Depends(get_db1), 
                       db2: sqlite3.Connection = Depends(get_db2)):
    win_agg = []
    cur = db.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    cur = db1.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    cur = db2.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    def sort_wins(row):
        return row["COUNT(won)"]
    
    win_agg.sort(reverse=True ,key=sort_wins)
    
    return win_agg[0:10]

def updateTop10Streaks(db: sqlite3.Connection = Depends(get_db),
            db1: sqlite3.Connection = Depends(get_db1), db2: sqlite3.Connection = Depends(get_db2)):
    streak_agg = []

    cur = db.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    cur = db1.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    cur = db2.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    def sort_streak(row):
        return row["streak"]
    
    streak_agg.sort(reverse=True, key=sort_streak)
    
    return streak_agg[0:10]

def main():
    streaks = updateTop10Streaks()
    wins = updateTop10Wins()
    
    for x in streaks:
        print(x)
        # redisClient.zadd()
        
    for y in wins:
        print(y)
 
if __name__ == "__main__":
    main()   