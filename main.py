from game_settings import game_settings_stage
from topdown_game import *

def setup():
    settings = game_settings_stage()  # Starts game settings module to do its thing to gain the settings
    gm = Game_Manager(settings)  # Pass the settings onto the game to actually run the darn thing
    gm.start_game()  # Kicks the game into gear

if __name__ == "__main__":
    setup()