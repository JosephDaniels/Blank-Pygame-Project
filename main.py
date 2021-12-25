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

    # SETUP
    manager = Game_Manager(settings)

    # GAME LOOP
    manager.start_loop()

def map_test():
    """ test of our own json map reader"""
    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = TiledMap("./maps/test_level.json")
    tiled_map.dump()
    running = True
    frame_num = 0

    # do a test render and see if it shows up correctly
    tiled_map.render_layer("ground", screen)
    tiled_map.render_layer("walls", screen)
    # tiled_map.render_layer("test", screen)  ## This really helped out!!!

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()

        pygame.time.delay(100)

if __name__ == "__main__":
    main_loop()