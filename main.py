from gamesettings_tkinter import GameSetupApp
import tkinter as tk
from topdown_game import *

def main_loop():
    # Tkinter Settings Window
    root = tk.Tk()
    root.withdraw()
    myapp = GameSetupApp(root)
    myapp.mainloop()
    settings = myapp.settings
    if myapp.start_game == True:
        ## Actual Game Loop
        root.destroy()
        do_game(settings)

def do_game(settings):
    p = Player(512,512,"images/player.png")
    manager = Game_Manager(settings)
    manager.add_player(p)
    manager.start_loop()

if __name__ == "__main__":
    main_loop()