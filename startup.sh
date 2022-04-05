# TODO: add all python and DB commands that need to be run
# and then Procfile

python3 Word_Validation_Service/wordsDB.py
uvicorn --port $PORT Word_Validation_Service.wordsAPI:app --reload
foreman start