class GameState:
    max_guesses = 6
    def __init__(self, user_id, game_id, guesses = []):
        self.user_id = user_id
        self.game_id = game_id
        self.guesses = guesses
    
    def eligible_guess(self):
        return len(self.guesses) < self.max_guesses
    
    def add_guess(self, guess: str):
        self.guesses.append(guess)