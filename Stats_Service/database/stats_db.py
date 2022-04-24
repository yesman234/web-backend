import sqlite3

print("Initializing the stats sharded databases...")

# TODO: update to create 3 separate DBs
databases_to_create = 1
stat_db_name = "StatDB"
sql_filename = "Stats_Service\database\stats.sql" # file is called from root directory
for i in range(databases_to_create):
    db = sqlite3.connect(stat_db_name + '_' + str(i))
    cursor = db.cursor()
    sql_file = open(sql_filename)
    cursor.executescript(sql_file.read()) 
    sql_file.close()
    db.commit()
    db.close()