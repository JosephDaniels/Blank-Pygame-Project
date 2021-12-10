import pygame
import time
import sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

class Game_Manager(object):
    """ Handles all the game objects,
        and manages the game stuff!!!"""
    def __init__(self):
        self.player = None
        self.actors = []
        self.objects = []
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Top Down Game")

    def add_player(self, player):
        self.player = player

    def start_loop(self):
        while self.running == True:
            ## HANDLE EVENTS
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                        break

            ## UPDATE PHYSICS AND POSITION
            self.player.update()

            ## BLIT ALL OBJECTS
            self.screen.fill((0,0,0))

            self.screen.blit(self.player.image, (self.player.x, self.player.y))

            pygame.display.flip()

            time.sleep(0.01)

class GameObject(object):
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

class Player(GameObject):
    def __init__(self, x, y, image_file):
        super().__init__(x, y, image_file)
        self.vx = 0

    def update(self):
        self.x += self.vx
        print ("player tick")

def test_game():
    p = Player(512,512,"images/player.png")
    manager = Game_Manager()
    manager.add_player(p)
    manager.start_loop()

if __name__ == "__main__":
    test_game()

