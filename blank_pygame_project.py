import pygame
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Game_Manager(object):
    """ Handles all the game objects,
        and manages the game stuff!!!"""
    def __init__(self):
        self.player = None
        self.actors = []
        self.objects = []
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Blank Project")

class Game_Object(object):
    def __init__(self, x, y, image_file):
        self.x = x
        self.y = y
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file)

    def get_rect(self):
        self.rect = self.image.get_rect()
        return self.rect

    def is_collided_with(self, target):
        rect1 = self.image.get_rect()
        rect1.topleft = (self.x,self.y)
        rect2 = target.image.get_rect()
        rect2.topleft = (target.x, target.y)
        return rect1.colliderect(rect2)
