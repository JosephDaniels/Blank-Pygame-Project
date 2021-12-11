import tkinter as tk
from tkinter import ttk, messagebox

class ControllerSettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        row = 0

        welcome_message = """
        Hi there.
        
        Please choose how you wish to control the game.
        """

        message = tk.Label(self, text=welcome_message)
        message.grid(column=0, row=row)
        row = row+1

        keyboard_button = tk.Button(self,
                                    text="Keyboard",
                                    command=self.apply_keyboard_settings)
        keyboard_button.grid(column=0, row=row)
        row = row+1

        joystick_button = tk.Button(self,
                                    text="Joystick",
                                    command=self.apply_joystick_settings)
        joystick_button.grid(column=0, row=row)
        row = row+1

        return_to_menu_button = tk.Button(self,
                                        text="Save & Return",
                                        command=self.save_and_return)
        return_to_menu_button.grid(column=0, row=row)
        row = row+1

    def save_and_return(self):
        print (self.master.settings)
        self.destroy()

    def apply_keyboard_settings(self):
        self.master.settings["Controller Preference"] = "Keyboard"
        message = tk.messagebox.showinfo(title="Controls switched.",
                                         message="Keyboard controls chosen.")
        print ("Keyboard chosen!")

    def apply_joystick_settings(self):
        self.master.settings["Controller Preference"] = "Joystick"
        message = tk.messagebox.showinfo(title="Controls switched.",
                                         message="Joystick controls chosen.")
        print("Joystick chosen!")

class GameSetupApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.settings = {
            "Default Controls"   :   True,
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

        quit_button = tk.Button(self,
                                    text="Quit Game",
                                    command=self.do_quit_game)
        quit_button.grid(column=0, row=row)
        row = row+1

    def do_quit_game(self):
        self.quit()

    def open_controller_settings(self):
        self.controller_settings_window = ControllerSettingsWindow(self)

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