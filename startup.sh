# TODO: add all python and DB commands that need to be run
# and then Procfile
#foreman start -e .env

cd Word_Validation_Service
python3 wordsDB.py
uvicorn wordsAPI:app --reload