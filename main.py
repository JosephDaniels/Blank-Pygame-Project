from gamesettings_tkinter import GameSetupApp
import tkinter as tk
from topdown_game import *

def main_loop():
    # Tkinter Settings Window
    root = tk.Tk()
    root.withdraw()
    app = GameSetupApp(root)
    app.mainloop()
    print ("after main loop")
    settings = app.settings
    if app.start_game == True:
        ## Actual Game Loop
        root.destroy()
        do_game(settings)

def do_game(settings):
    print ("Starting the game...")
    manager = Game_Manager(settings)
    manager.start_loop()

if __name__ == "__main__":
    main_loop()