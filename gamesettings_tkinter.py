import tkinter as tk
from tkinter import ttk, messagebox

class GameSetupApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.settings = {
        }
        self.start_game = False
        self.create_widgets()

    def create_widgets(self):
        row = 0

        welcome_message = """
        Welcome to the game setup screen. Please choose an option from below.
        """

        message = tk.Label(self, text=welcome_message)
        message.grid(column=0, row=row)
        row = row+1

        controller_settings_button = tk.Button(self,
                                    text="Controller Settings",
                                    command=self.open_controller_settings)
        controller_settings_button.grid(column=0, row=row)
        row = row+1

        video_settings_button = tk.Button(self,
                                    text="Video Settings",
                                    command=self.open_video_settings)
        video_settings_button.grid(column=0, row=row)
        row = row+1

        audio_settings_button = tk.Button(self,
                                    text="Sound Settings",
                                    command=self.open_sound_settings)
        audio_settings_button.grid(column=0, row=row)
        row = row+1

        start_game_button = tk.Button(self,
                                    text="Start Game",
                                    command=self.do_start_game)
        start_game_button.grid(column=0, row=row)
        row = row+1

    def open_controller_settings(self):
        pass

    def open_video_settings(self):
        pass

    def open_sound_settings(self):
        pass

    def do_start_game(self):
        print ("starting the game!")
        self.start_game = True
        self.quit()

def test_1():
    root = tk.Tk()
    root.withdraw()
    myapp = GameSetupApp(root)
    myapp.mainloop()

if __name__ == "__main__":
    test_1()