"""This file implements the actual playable game"""


import time
import sys
import logging

import pygame

from gameobject import GameObject
from animation import AnimationSequence
from maps import *

logging.basicConfig(filename="game.log", level=logging.DEBUG)


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class Viewport(object):
    def __init__(self, screen,
                 viewport_width=SCREEN_WIDTH,
                 viewport_height=SCREEN_HEIGHT):
        self.screen = screen
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        ## This is the viewport origin in game coordinates
        self.game_x, self.game_y = 0, 0

    def shift_viewport(self, dx, dy):
        self.game_x += dx
        self.game_y += dy

    def set_origin(self, x, y):
        self.game_x, self.game_y = x, y

    def render(self, obj):
        screen_x = int(-(self.game_x) + (obj.x))
        screen_y = int(-(self.game_y) + (obj.y))
        obj.draw(self.screen, screen_x, screen_y)
        logging.debug(msg="screen_x=%s screen_y=%s" % (screen_x, screen_y))

class Game_Manager(object):
    """ Handles all the game objects,
        and manages the game stuff!!!"""
    def __init__(self, settings={}, map_name=""):
        self.map_name = "./maps/"+map_name
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.viewport = Viewport(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.viewport.set_origin(-SCREEN_WIDTH/2,
                                 -SCREEN_HEIGHT/2)
        if settings == {}:
            pass
        else:
            self.settings = settings
            self.load_settings()

            logging.debug("Manager initialized. Settings :"+str(self.settings))

        # SPECIAL MAIN PLAYER CODE
        self.main_player = Player(0, 0)
        self.players = []  # These are the other player entities

        # OTHER STUFF
        self.actors = []  # These are the enemy creatures
        self.pickups = []  # These are items that are instantly "picked up" by player entities
        self.furniture = []  # These are just all the interactible furniture and set pieces
        self.projectiles = []  # A list of moving bullets and arrows

        # START FLAG
        self.running = True

        # Creating a lot of debug msgs!!!
        self.tiled_map = TiledMap(self.map_name,
                                  -SCREEN_WIDTH/2,
                                  -SCREEN_HEIGHT/2)

        self.anim_counter = 2
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Top Down Game")

    def add_main_player(self, player):
        # Add the main character that the game focuses on
        self.main_player = player
        logging.debug("player added: %s" % str(player))


    def add_player(self, player):
        # Adds additional players to the game
        self.players.append(player)

    def load_settings(self):
        if self.settings["Controller Preference"] == "Joystick":
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(0)

    def handle_escape_key_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
            pygame.quit()
            sys.exit()

    def handle_keyboard_events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_escape_key_events(event)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.move_right()
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.move_left()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    player.move_up()
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.move_down()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.stop_move_x()
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.stop_move_x()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    player.stop_move_y()
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.stop_move_y()

    def handle_joystick_events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_escape_key_events(event)
            if event.type == pygame.JOYHATMOTION:
                if event.value == (1, 0):
                    print ("Move right")
                    player.move_right()
                elif event.value == (-1, 0):
                    print ("Move Left")
                    player.move_left()
                elif event.value == (0, 1):
                    print ("Move Up")
                    player.move_up()
                elif event.value == (0, -1):
                    print ("Move Down")
                    player.move_down()
                elif event.value == (0, 0):
                    print ("Stop Move")
                    player.stop_move()

    def start_game(self):
        # This will fail if settings are not set properly
        while self.running == True:
            # HANDLE EVENTS
            if self.settings["Controller Preference"] == "Keyboard":
                self.handle_keyboard_events(self.main_player)
            elif self.settings["Controller Preference"] == "Joystick":
                self.handle_joystick_events(self.main_player)

            # UPDATE PHYSICS AND POSITION
            self.main_player.update()

            # for player in self.players:
            #     player.update()

            # for actor in self.actors:
            #     actor.update()

            # HANDLE COLLISIONS

            for tile in self.tiled_map.layers["walls"].tiles:
                if player.is_collided_with(tile):
                    print ("COLLISION!!!")

            self.viewport.set_origin(self.main_player.x - SCREEN_WIDTH / 2,
                                     self.main_player.y - SCREEN_HEIGHT / 2)

            # RENDER STUFF

            # MAPS
            self.screen.fill((0,0,0))

            self.viewport.render(self.tiled_map.layers["ground"])

            for layer_name in self.tiled_map.layers.keys():
                if layer_name != "ground":
                    self.viewport.render(self.tiled_map.layers[layer_name])

            # PLAYER
            self.viewport.render(self.main_player)

            pygame.display.flip()
            time.sleep(0.01)

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vx = 0
        self.vy = 0
        self.anim_counter = 5
        self.load_animations()
        self.current_frame = 0
        self.current_animation = self.walk_left_anim

    def load_animations(self):
        self.scale_factor = 3
        self.sprite_sheet = pygame.image.load("./images/sprite_sheet.gif")
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (400*self.scale_factor,
                                                                       780*self.scale_factor))
        self.walk_left_anim = AnimationSequence(self.sprite_sheet,
                                                8*self.scale_factor,
                                                453*self.scale_factor,
                                                24*self.scale_factor,
                                                28*self.scale_factor,8)
        self.walk_right_anim = AnimationSequence(self.sprite_sheet,
                                                 198*self.scale_factor,
                                                 453*self.scale_factor,
                                                 23*self.scale_factor,
                                                 28*self.scale_factor, 8)
        self.walk_up_anim = AnimationSequence(self.sprite_sheet,
                                              9*self.scale_factor,
                                              486*self.scale_factor,
                                              23*self.scale_factor,
                                              28*self.scale_factor, 8)
        self.walk_down_anim = AnimationSequence(self.sprite_sheet,
                                                200*self.scale_factor,
                                                486*self.scale_factor,
                                                22*self.scale_factor,
                                                28*self.scale_factor, 8)

    def update(self):
        if abs(self.vx) == 4 and abs(self.vy) == 4:
            self.x += self.vx*0.7
            self.y += self.vy*0.7
        else:
            self.x += self.vx
            self.y += self.vy
        if self.anim_counter == 0:
            self.current_frame += 1
            self.anim_counter = 5
        else:
            self.anim_counter -= 1
        if self.current_frame >= self.current_animation.num_frames:
            self.current_frame = 0
        if self.vx == 0 and self.vy == 0:
            self.current_frame = 0

    def draw(self, surface, dest_x, dest_y):
        # Draw always draws to screen coordinates
        self.current_animation.draw(surface,
                                    dest_x,
                                    SCREEN_HEIGHT - dest_y,
                                    self.current_frame)
    def move_right(self):
        self.current_animation = self.walk_right_anim
        self.vx = 4

    def move_left(self):
        self.current_animation = self.walk_left_anim
        self.vx = -4

    def move_up(self):
        self.current_animation = self.walk_up_anim
        self.vy = 4

    def move_down(self):
        self.current_animation = self.walk_down_anim
        self.vy = -4

    def stop_move(self):
        self.vx = 0
        self.vy =0

    def stop_move_x(self):
        self.vx = 0

    def stop_move_y(self):
        self.vy = 0

def main_loop_test_settings():
    pygame.init()
    settings = {
        "Controller Preference"  :  "Keyboard"
    }
    gm = Game_Manager(settings, map_name="forest_glade_v1.json")
    gm.start_game()


if __name__ == "__main__":
    main_loop_test_settings()