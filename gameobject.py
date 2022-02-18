import pygame

class GameObject(object):
    def __init__(self, x, y, width, height):
        # X and Y in game world coordinates
        self.x = x # Center x
        self.y = y # Center y
        self.bbox_left = -width/2
        self.bbox_top = -height/2

    def draw(self, surface, dest_x, dest_y):
        ## Draws to game coordinates
        dest_y = -dest_y
        surface.blit(self.image, (dest_x,
                                  dest_y))

    def resize(self, new_width, new_height):
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def get_rect(self):
        return pygame.Rect(self.x-self.width/2, self.y-self.height/2, width, height)

    def is_collided_with(self, target):
        # Tests for collision in game coordinates
        rect1 = self.get_rect()
        rect2 = target.get_rect()
        return rect1.colliderect(rect2)