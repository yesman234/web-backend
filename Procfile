validate: uvicorn --port $PORT Word_Validation_Service.wordsAPI:app --reload
stats: uvicorn --port $PORT Stats_Service.api:app --reload
answer: sh -c "cd ./Answer_Checking_Service/ && uvicorn --port $PORT api:app --reload"
