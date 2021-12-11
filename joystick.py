import pygame
import time
import sys

def test_1():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    screen = pygame.display.set_mode((600,400))
    while pygame.joystick.get_init():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                print (event)
        time.sleep(0.06)

if __name__ == "__main__":
    test_1()