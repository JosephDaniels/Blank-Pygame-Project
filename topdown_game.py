import pygame
import time
import sys
from animation import AnimationSequence

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class Game_Manager(object):
    """ Handles all the game objects,
        and manages the game stuff!!!"""
    def __init__(self, settings):
        self.settings = settings
        self.load_settings()
        print ("Manager initialized. Settings :"+str(self.settings))

        ## Add players to the game.
        self.players = []
        for num_players in range(self.settings["Number of Players"]):
            player = Player(150*num_players,512,"images/player.png")
            self.players.append(player)
        self.actors = []
        self.objects = []
        self.running = True
        self.background = GameObject(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,"images/test_background_DO_NOT_SHIP.jpg")
        self.background.resize(1024, 768)
        self.anim_counter = 2
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Top Down Game")

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

    def start_loop(self):
        while self.running == True:
            ## HANDLE EVENTS
            if self.settings["Controller Preference"] == "Keyboard":
                self.handle_keyboard_events(self.players[0])
            elif self.settings["Controller Preference"] == "Joystick":
                self.handle_joystick_events(self.players[0])

            ## UPDATE PHYSICS AND POSITION
            for player in self.players:
                player.update()
            for actor in self.actors:
                actor.update()

            ## DISPLAY ALL OBJECTS

            ## BACKGROUND
            self.background.draw(self.screen)
            ## PLAYER
            for player in self.players:
                player.draw(self.screen)

            pygame.display.flip()

            time.sleep(0.01)

class GameObject(object):
    def __init__(self, x, y, image_file):
        self.x = x
        self.y = y
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file)

    def draw(self, surface):
        ## Draws to actual game coordinates
        surface.blit(self.image, (self.x-self.image.get_width()/2, SCREEN_HEIGHT-self.y-self.image.get_height()/2))

    def resize(self, new_width, new_height):
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def get_rect(self):
        self.rect = self.image.get_rect()
        return self.rect

    def is_collided_with(self, target):
        rect1 = self.image.get_rect()
        rect1.topleft = (self.x,self.y)
        rect2 = target.image.get_rect()
        rect2.topleft = (target.x, target.y)
        return rect1.colliderect(rect2)

class Player(GameObject):
    def __init__(self, x, y, image_file):
        super().__init__(x, y, image_file)
        self.vx = 0
        self.vy = 0
        self.anim_counter = 5
        self.load_animations()
        self.current_frame = 0
        self.current_animation = self.walk_left_anim

    def load_animations(self):
        self.scale_factor = 4
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

    def draw(self, surface):
        self.current_animation.draw(surface, self.x-self.current_animation.w/2,
                                    SCREEN_HEIGHT-self.y-self.current_animation.h/2,
                                    self.current_frame)

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

def test_game():
    p = Player(512,512,"images/player.png")
    settings = {}
    manager = Game_Manager(settings)
    manager.add_player(p)
    manager.start_loop()

if __name__ == "__main__":
    test_game()

