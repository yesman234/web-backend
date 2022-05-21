from curses import curs_set
from datetime import date, datetime
from http import HTTPStatus
import httpx
import datetime
import json
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
import Game_State
from root import GameState

app = FastAPI()

BASE_URL = "http://localhost:9999/api/"
VALIDATOR_ENDPOINT = BASE_URL + "v1/"
STATS_ENDPOINT = BASE_URL + "v2/"
ANSWER_ENDPOINT = BASE_URL + "v3/"
GAME_STATE_ENDPOINT = BASE_URL + "v4/"
YEAR = 2022


@app.post("/game/new")
def newGame(username: str):
    today_game_id = (datetime.date.today() - datetime.date(YEAR, 1, 1)).days

    resp = httpx.post(STATS_ENDPOINT + "user_id", params={"username": username})

    user_id = json.loads(resp.content.decode('utf-8'))['user_id']

    req_body = {
        'user_id': user_id,
        'game_id': today_game_id
    }

    resp = httpx.post(GAME_STATE_ENDPOINT + "create", data=json.dumps(req_body))

    return {
        "status": "new",
        "user_id": user_id,
        "game_id": today_game_id
    }

@app.post("/game")
def guessWord(user_id: str, guess: str):
     # TODO: bulk of work likely here
    # 1. verify guess with word validation service
    resp = httpx.post(VALIDATOR_ENDPOINT + "WordValidations", data=json.dumps({"word": guess}))
    

    is_valid = bool(json.loads(resp.content.decode('utf-8'))['word_valid'])

    if not is_valid:
        return HTTPStatus.BAD_REQUEST

    # 2. check that user has guesses remaining (get game state)
    resp = httpx.get(GAME_STATE_ENDPOINT + 'restore/' + user_id)

    cur_game_state = GameState.GameState.httpx_to_GameState(json.loads(json.loads(resp.content.decode('utf-8'))['user_id']))

    if cur_game_state.guesses_remaining() == 0:
        return HTTPStatus.BAD_REQUEST

    # if 1 and 2 are true
    # 3. Record the guess and update number of guesses remaining
    # 4. Check to see if guess correct
    resp = httpx.post(ANSWER_ENDPOINT + 'check', data=json.dumps({"word": guess, "timestamp": str(datetime.datetime.now().timestamp())}))

    letter_check = json.loads(resp.content.decode('utf-8'))

    game_win = True
    for letter in letter_check:
        if letter != 'green':
            game_win = False
            break
    
    # update game state
    resp = httpx.put(GAME_STATE_ENDPOINT + 'update/' + user_id + '/' + guess)
    cur_game_state = GameState.GameState.httpx_to_GameState(json.loads(json.loads(resp.content.decode('utf-8'))['user_id']))

    print("Guess Remaining:" + str(cur_game_state.guesses_remaining()))
    
    if game_win or cur_game_state.guesses_remaining() == 0:
        httpx.post(STATS_ENDPOINT + 'games', data=json.dumps({
            "user_id": cur_game_state.user_id,
            "game_id": cur_game_state.game_id,
            "finished": str(datetime.datetime.now().timestamp()),
            "guesses": cur_game_state.guesses,
            "won": game_win
        }))

        resp = httpx.get(STATS_ENDPOINT + 'games/' + cur_game_state.user_id)

        return json.loads(resp.content.decode('utf-8'))
    
    correct = []
    present = []
    for i in range(len(letter_check)):
        if letter_check[i] == 'green':
            correct.append(guess[i])
        elif letter_check[i] == 'yellow':
            present.append(guess[i])

    return {
        "remaining": cur_game_state.guesses_remaining(),
        "status": "incorrect",
        "letters": {
            "correct": correct,
            "present": present
        }
    }