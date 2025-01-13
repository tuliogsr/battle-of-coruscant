import json

class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start game in an inactive state.
        self.game_active = False
        
        # High score should never be reset.
        self.high_score = 0
        self.load_high_score()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Save the high score to a file."""
        try:
            with open('high_score.json', 'w') as f:
                json.dump(self.high_score, f)
        except IOError:
            print("Unable to save high score.")

    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open('high_score.json', 'r') as f:
                self.high_score = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.high_score = 0