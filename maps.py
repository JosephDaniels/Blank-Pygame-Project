import pygame
from csv import


class MapLevel(object):
    def __init__(self, filename):
        self.filename = filename
        self.load_tiles()

    def load_tiles(self):
        pass