from fastapi import FastAPI

app = FastAPI()


# Starting a new game. The client should supply a user ID and game ID when a game starts. If the user has already played the game, they should receive an error.
@app.post('/create')
def start_a_new_game():
    return {'hello': 'world'}

# Updating the state of a game. When a user makes a new guess for a game, record the guess and update the number of guesses remaining. If a user tries to guess more than six times, they should receive an error.
# Note: you do not need to check whether the guess is valid, if the guess is correct, or report on the placement of the letters in the answer. This functionality was completed in Project 2.
@app.put('/update')
def update_state_of_a_game():
    return {'hello': 'world'}

# Restoring the state of a game. Upon request, the user should be able to retrieve an object containing the current state of a game, including the words guessed so far and the number of guesses remaining.
@app.get('/restore')
def restore_state_of_a_game():
    return {'hello': 'world'}
