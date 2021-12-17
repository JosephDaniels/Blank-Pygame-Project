import pygame
import pytmx

class MapLevel(object):
    def __init__(self, filename):
        """creates a MapLevel object from the given Tiled json file"""
        pass

    def render_layer(self, layer_name):
        pass


def test1():
    """loads and renders a single level"""

    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = pytmx.util_pygame.load_pygame("./maps/test_level.tmx")
    ground_layer = tiled_map.layernames["ground"]
    wall_layer = tiled_map.layernames["walls"]
    tile_images = tiled_map.images

    running = True
    frame_num = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0,0,0))

        # render the ground layer by iterating through all the tiles
        for x,y, gid in ground_layer:
            tile_props = tiled_map.get_tile_properties(x,y, ground_layer)
            img = tile_images[gid]
            if img:
                screen.blit(img, (x*img.get_width(), y*img.get_height() ))

        # render the wall layer by iterating through all the tiles
        for x,y, gid in wall_layer:
            img = tile_images[gid]
            if img:
                screen.blit(img, (x*img.get_width(), y*img.get_height() ))
        pygame.display.flip()
        pygame.time.delay(100)
    pygame.quit()



if __name__ == "__main__":
    test1()
