import pygame
import pytmx
import json


class TileImage(object):
    """create the pygame render image for a given tile"""
    def __init__(self, tmx_gid, src_img):
        self.ident = tmx_gid
        self.img = src_img.copy() # make a copy so rotations don't clobber the original
        # check if the image is rotated...
        self.flipH = False
        self.flipV = False
        self.flipXY = False
        if tmx_gid & 0x20000000:
            self.flipXY = True  # flip diagonally in the xy direction
            self.img = pygame.transform.flip(self.img, flip_x=True, flip_y=True)
        if tmx_gid & 0x40000000:
            self.flipV = True  # flip vertically
            self.img = pygame.transform.flip(self.img, flip_x=False, flip_y=True)
        if tmx_gid & 0x80000000:
            self.flipH = True # flip horizontally
            self.img = pygame.transform.flip(self.img, flip_x = True, flip_y = False)


class MapLayer(object):
    """  creates a layer plane from layer data decoded from the tmx file """
    def __init__(self, parent_map, decoded_layer_data):
        self.parent = parent_map
        self.height = parent_map.height
        self.width = parent_map.width
        self.tiles = decoded_layer_data["data"]  # is a list of gids for the layer
        # scan through the tile gids (so we can cache all the possible rotated tile images)
        for gid in self.tiles:
            self.parent.cache_tile_gid(gid)

    def render(self, target_surface):
        pass


class MapLevel(object):
    def __init__(self, filename):
        """creates a MapLevel object from the given Tiled json file"""
        self.filename = filename
        data = json.load(open(filename))
        # decode
        self.width = data["width"]
        self.height = data["height"] # height in tiles
        self.tile_height = data["tileheight"]
        self.tile_width = data["tilewidth"]

        # load the tile source images and save them by filename and gid
        self.images_by_filename = {} # the original tile images
        self.images_by_gid = {}
        for tile_set in data["tilesets"]:
            for tile in tile_set["tiles"]:
                tmx_gid = tile["id"]
                filename = tile["image"]
                # check if the image file has been loaded already
                if not(filename in self.images_by_filename):
                    img = pygame.image.load("./maps/"+filename).convert()
                    self.images_by_filename[filename] = img
                    self.images_by_gid[tmx_gid] = img

        self.layers = {} # index the layers by their name
        # load each layer
        all_layers = data["layers"]
        for layer_data in all_layers:
            name = layer_data["name"]
            self.layers[name] = MapLayer(self, layer_data)


    def cache_tile_rotation(self, gid, img):
        """in the tmx file format, a tile's gid also determines the rotation of
        a tile image. So this will cache the rotated tile image so that rendering
        is more efficient"""
        if not gid in self.tile_images.keys():
            self.tile_images[gid] = TileImage(gid)


    def dump(self):
        print(f"tmx json file is: {self.filename}")
        print(f"width: {self.width}, height:{self.height}")
        print(f"There are {len(self.images_by_filename)} tile images loaded")
        print(f"There are {len(self.layers)} layers loaded")


    def render_layer(self, layer_name, target_surface):
        # render the ground layer by iterating through all the tiles
        i = 0
        j = 0
        layer = self.layers[layer_name]
        map_width = self.width
        for tile in layer.tiles:
            img = None
            if img:
                target_surface.blit(img, (i * tile_width, j * tile_height))
            i += 1
            if i >= map_width:
                i = 0
                j += 1



def test2():
    """ test of our own json map reader"""
    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = MapLevel("./maps/test_level.json")
    tiled_map.dump()
    running = False
    frame_num = 0

    # do a test render and see if it shows up correctly
    tiled_map.render_layer("ground", screen)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.time.delay(100)
    pygame.quit()


if __name__ == "__main__":
    test2()
