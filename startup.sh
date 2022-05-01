python3 Word_Validation_Service/wordsDB.py
python3 Stats_Service/database/stats_db.py
python3 Stats_Service/database/fake_stat_data.py

foreman start -e .env -m validate=1,stats=1,answer=1,game_state=1 &

./traefik --configFile=traefik.toml
