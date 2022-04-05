validate: uvicorn --port $VALIDATE_SERVICE_PORT Word_Validation_Service.wordsAPI:app --reload
answer: sh -c "cd ./Answer_Checking_Service/ && uvicorn --port $ANSWER_SERVICE_PORT api:app --reload"
