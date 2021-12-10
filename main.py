import gamesettings_tkinter
import topdown_game

def main_loop():
    do_settings()

def do_settings():
    root = tk.Tk()
    root.withdraw()
    myapp = GameSetupApp(root)
    myapp.mainloop()

def do_game():
    p = Player(512,512,"images/player.png")
    manager = Game_Manager()
    manager.add_player(p)
    manager.start_loop()

if __name__ == "__main__":
    main_loop()