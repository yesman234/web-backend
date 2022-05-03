from email.policy import HTTP
from http import HTTPStatus
from fastapi import FastAPI
from pydantic import BaseModel
from .GameState import GameState
from types import SimpleNamespace
import redis
import json

app = FastAPI()

# Setup redis db
r = redis.Redis()

class NewGame(BaseModel):
    user_id: str
    game_id: int

# Starting a new game. The client should supply a user ID and game ID when a game starts. If the user has already played the game, they should receive an error.
@app.post('/create')
def start_a_new_game(new_game: NewGame):
    # User account exists
    if r.exists(new_game.user_id):
        cur_gamestate: GameState = GameState.json_to_GameState(json.loads(r.get(new_game.user_id), object_hook=lambda d: SimpleNamespace(**d)))

        if new_game.game_id in cur_gamestate.prev_game_ids or new_game.game_id == cur_gamestate.game_id:
            return HTTPStatus.BAD_REQUEST
        
        cur_gamestate.prev_game_ids.append(cur_gamestate.game_id)
        cur_gamestate.game_id = new_game.game_id

        r.set(cur_gamestate.user_id, json.dumps(cur_gamestate, default=vars))

        return HTTPStatus.OK
    # New user account
    else:
        new_game_state = GameState(new_game.user_id, new_game.game_id)
        r.set(new_game_state.user_id, json.dumps(new_game_state, default=vars))
        
        return HTTPStatus.OK

# Updating the state of a game. When a user makes a new guess for a game, record the guess and update the number of guesses remaining. If a user tries to guess more than six times, they should receive an error.
# Note: you do not need to check whether the guess is valid, if the guess is correct, or report on the placement of the letters in the answer. This functionality was completed in Project 2.
@app.put('/update')
def update_state_of_a_game():
    return {'hello': 'world'}

# Restoring the state of a game. Upon request, the user should be able to retrieve an object containing the current state of a game, including the words guessed so far and the number of guesses remaining.
@app.get('/restore')
def restore_state_of_a_game():
    return {'hello': 'world'}
