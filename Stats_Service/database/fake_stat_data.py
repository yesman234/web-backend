#!/usr/bin/env python3

import contextlib
import datetime
import random
import sqlite3
import uuid
from db_constants import total_databases, stat_db_name, db_file_extension

import faker

NUM_STATS = 1_000_000
NUM_USERS = 100_000
YEAR = 2022

random.seed(YEAR)
fake = faker.Faker()
faker.Faker.seed(YEAR)
cur_user_ids = []
print("Beginning to insert fake stat data...")
for db_num in range(total_databases):
    cur_db = stat_db_name + str(db_num) + db_file_extension
    with contextlib.closing(sqlite3.connect(cur_db)) as db:
        for _ in range(NUM_USERS):
            try:
                username = str(fake.simple_profile()['username'])
                user_id = str(uuid.uuid4())
                cur_user_ids.append(user_id)
                db.execute('INSERT INTO users(user_id, username) VALUES(?, ?)', [
                           user_id, username])

            except sqlite3.IntegrityError:
                continue
        db.commit()
        print("Finished Users table")
        jan_1 = datetime.date(YEAR, 1, 1)
        today = datetime.date.today()
        num_days = (today - jan_1).days
        for _ in range(NUM_STATS):
            try:
                user_id = cur_user_ids[random.randint(
                    0, len(cur_user_ids) - 1)]
                game_id = random.randint(1, num_days)
                finished = jan_1 + \
                    datetime.timedelta(random.randint(0, num_days))
                # N.B. real game scores aren't uniformly distributed...
                guesses = random.randint(1, 6)
                # ... and people mostly play to win
                won = random.choice([False, True, True, True])
                db.execute(
                    """
                    INSERT INTO games(user_id, game_id, finished, guesses, won)
                    VALUES(?, ?, ?, ?, ?)
                    """,
                    [user_id, game_id, finished, guesses, won]
                )
            except sqlite3.IntegrityError:
                continue
        db.commit()
        print("Finished Games table")
        cur_user_ids.clear()
