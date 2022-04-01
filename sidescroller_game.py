import pygame
import sys
import time
from gameobject import GameObject
from animation import AnimationSequence

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

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
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.viewport = Viewport(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.viewport.set_origin(-SCREEN_WIDTH/2,
                                 -SCREEN_HEIGHT/2)

        # SPECIAL MAIN PLAYER CODE
        self.main_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 166, 210)

        # OTHER STUFF
        self.actors = []  # These are the enemy creatures
        self.pickups = []  # These are items that are instantly "picked up" by player entities
        self.furniture = []  # These are just all the interactible furniture and set pieces
        self.projectiles = []  # A list of moving bullets and arrows

        # START FLAG
        self.running = True
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Side Scroller Game")

    def start_game(self):
        while self.running == True:

            # HANDLE EVENTS
            self.handle_events()

            # UPDATE PHYSICS AND POSITION
            self.main_player.update()

            # for player in self.players:
            #     player.update()

            # for actor in self.actors:
            #     actor.update()

            # HANDLE COLLISIONS

            # RENDER STUFF

            # MAPS
            self.screen.fill((0,0,0))

            # PLAYER
            self.main_player.draw(self.screen, self.main_player.x, self.main_player.y)

            pygame.display.flip()
            time.sleep(0.01)

    def handle_escape_key_events(self, event):
        self.running = False
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.handle_escape_key_events()
                if event.key == pygame.K_RIGHT:
                    self.main_player.move_right()
                if event.key == pygame.K_LEFT:
                    self.main_player.move_left()
            if event.type == pygame.KEYUP:
                if event.key == (pygame.K_RIGHT):
                    self.main_player.stop_move_right()
                elif event.key == (pygame.K_LEFT):
                    self.main_player.stop_move_left()

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.anim_counter = 0
        self.load_animations()
        self.current_frame = 0
        self.current_animation = self.idle_right_anim

    def load_animations(self):
        self.scale_factor = 3
        self.idle_left_image = pygame.image.load("./images/female_idle_left.png")
        self.idle_right_image = pygame.image.load("./images/female_idle_right.png")
        self.sprite_sheet_left = pygame.image.load("./images/female_run_cycle_left.png")
        self.sprite_sheet_right = pygame.image.load("./images/female_run_cycle_right_revised.png")

        # self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (400*self.scale_factor,
        #                                                                780*self.scale_factor))

        self.idle_left_anim = AnimationSequence(self.idle_left_image,
                                           0,
                                           0,
                                           150,
                                           189,
                                           1)

        self.idle_right_anim = AnimationSequence(self.idle_right_image,
                                           0,
                                           0,
                                           150,
                                           189,
                                           1)

        self.walk_left_anim = AnimationSequence(self.sprite_sheet_left,
                                                0,
                                                0,
                                                150,
                                                189,
                                                18)

        self.walk_right_anim = AnimationSequence(self.sprite_sheet_right,
                                                0,
                                                0,
                                                150,
                                                189,
                                                18)

    def update(self):
        # handle the "physics"
        self.x += self.vx

        # handle the animation updates
        if self.anim_counter == 0:
            self.current_frame += 1
            self.anim_counter = 5
        else:
            self.anim_counter -= 1

        if self.current_frame >= self.current_animation.num_frames:
            self.current_frame  = 0



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

    def stop_move_left(self):
        self.current_animation = self.idle_left_anim
        self.vx = 0

    def stop_move_right(self):
        self.current_animation = self.idle_right_anim
        self.vx = 0

    def stop_move_y(self):
        self.vy = 0

def test_1():
    pygame.init()
    gm = Game_Manager()
    gm.start_game()

if __name__ == "__main__":
    test_1()