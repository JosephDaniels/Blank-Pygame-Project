import pygame
import pytmx
import json

class TileImage(object):
    def __init__(self, ident, filename):
        self.ident = ident
        self.filename = filename
        self.img = pygame.image.load("./maps/"+filename)


class MapLayer(object):
    def __init__(self):
        self.tiles = []
        self.height = 0
        self.width = 0

    def render(self, target_surface):
        pass


class MapLevel(object):
    def __init__(self, filename):
        """creates a MapLevel object from the given Tiled json file"""
        self.filename = filename
        data = json.load(open(filename))
        # de code
        self.width = data["width"]
        self.height = data["height"] # height in tiles
        self.layers = data["layers"]
        self.tile_height = data["tileheight"]
        self.tile_width = data["tilewidth"]
        # load the tile images
        self.tileimages = {}
        for tileset in data["tilesets"]:
            for tile in tileset["tiles"]:
                ident = tile["id"]
                filename = tile["image"]
                self.tileimages[ident] = TileImage(ident, filename)




    def dump(self):
        print(self.filename)
        print(f"width: {self.width}, height:{self.height}")


    def render_layer(self, layer_name):
        pass


def test1():
    """loads and renders a single level"""

    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = pytmx.util_pygame.load_pygame("./maps/test_level.tmx")
    ground_layer = tiled_map.layernames["ground"]
    ground_props = tiled_map.get_tile_properties_by_layer(0)
    for g in ground_props:
        print(g)

    wall_layer = tiled_map.layernames["walls"]
    tile_images = tiled_map.images
    keys = wall_layer.properties.keys()
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
            img = tile_images[gid]
            if img:
                screen.blit(img, (x*img.get_width(), y*img.get_height() ))

        # render the wall layer by iterating through all the tiles
        for x,y, gid in wall_layer:
            img = tile_images[gid]
            if img:
                props = tiled_map.get_tile_properties(x,y,1)
                print(props)
                screen.blit(img, (x*img.get_width(), y*img.get_height() ))

        pygame.display.flip()
        pygame.time.delay(100)
    pygame.quit()



def test2():
    """ test of our own json map reader"""
    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = MapLevel("./maps/test_level.json")
    tiled_map.dump()
    running = False
    frame_num = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0,0,0))

        # render the ground layer by iterating through all the tiles
        i = 0
        j = 0
        for tile in  ground_layer.tiles:
            img = None
            if img:
                screen.blit(img, (i*tile_width, j*tile_height))
            i += 1
            if i>=map_width:
                i = 0
                j += 1


        pygame.display.flip()
        pygame.time.delay(100)
    pygame.quit()


if __name__ == "__main__":
    test2()
