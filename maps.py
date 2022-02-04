import pygame
import json

""""
BEWARE: HERE BE DRAGONS

so after some messing around with Tiled's tmx format map files,
be aware that the tile gid is offset by one compared to what it is as map data.

The reason is, is that zeroes are equal to non-tiles (NULL)
but, a tile id of zero is allowed.

So all tile ids need to be incremented +1 in order to match the map data!!! (BAD)

They should not have allowed zero as a tile id!!! SO CONFUSING!!!

BEWARE: MORE ISSUES

ABANDON HOPE ALL YEE WHO ENTER

Okay so we determined that the flip horizontal bits for tiles really means
ROTATE 90 degrees horizontal.

This is important because otherwise you're screwed!!!

There's no way to flip an arrow turn sideways just by flipping it up and down left and right!

You must ROTATE!!!

Turns out FLIP_DIAGONAL is actually a combination of two moves: 

Flip vertical THEN a rotation of -90 degrees.

( misnomer from the documentation, it literally calls it flip
when it actually wants you to do something else)
"""


class MapLayer(object):
    """  creates a layer plane from layer data decoded from the tmx file """
    def __init__(self,
                 parent_map,
                 decoded_layer_data):
        self.x, self.y = parent_map.x, parent_map.y
        self.parent_map = parent_map
        self.height = parent_map.height
        self.width = parent_map.width
        self.tiles = decoded_layer_data["data"]  # is a list of gids for the layer
        # scan through the tile gids (so we can cache all the possible rotated tile images)
        for gid in self.tiles: # scan the gids in the current layer
            if gid != 0:
                self.parent_map.cache_tile_rotation(gid) # ...and have the parent TileMap cache any rotations

    def draw(self, target_surface,
             dest_x,
             dest_y):
        dest_x, dest_y = int(dest_x), int(dest_y)
        ## Draws to game coordinates
        dest_y = -dest_y
        # render the ground layer by iterating through all the tiles
        i = 0
        j = 0
        map_width = self.width
        tile_width, tile_height = 64, 64
        for gid in self.tiles:
            if gid != 0:
                img = self.parent_map.images_by_gid[gid]
                target_surface.blit(img, (dest_x + i * tile_width,
                                          dest_y + j * tile_height))
            i += 1
            if i >= map_width:
                i = 0
                j += 1

    def is_collided_with(self, target):
        rect1 = self.image.get_rect()
        rect1.topleft = (self.x,self.y)
        rect2 = target.image.get_rect()
        rect2.topleft = (target.x, target.y)
        return rect1.colliderect(rect2)


class TiledMap(object):
    def __init__(self, filename, x, y):
        """creates a MapLevel object from the given Tiled json file"""
        self.x, self.y = x, y  # Game coordinates / Origin
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
                tmx_gid = tile["id"]+1  ## Tiled increments all tiles by +1 because 0 is equivalent to blank
                ## also some tiles are gid 0 and are therefore gid 1
                ## I know it's really confusing ><
                ## So a gid of 0 is actually a gid of 1
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


    def cache_tile_rotation(self, gid):
        """in the tmx file format, a tile's gid also determines the rotation of
        a tile image. So this will cache the rotated tile image so that rendering
        is more efficient"""
        ## This is just to offset it so that it obeys Tiled's naming scheme
        if not gid in self.images_by_gid.keys(): # if not already in cache, must be rotated...
            print (f"gid = {gid}")
            masked_gid = gid & 0x1FFFFFFF  # mask off all bits except upper 3 bits
            print(f"masked id = {masked_gid}")
            rotation_gid = gid & 0xE0000000  # mask off upper 3 bits
            image = self.images_by_gid[masked_gid]  ## ERROR
            if rotation_gid & 0x20000000:  # Flip diagonal
                image = pygame.transform.flip(image, flip_x=False, flip_y=True)
                image = pygame.transform.rotate(image, -90)
            if rotation_gid & 0x40000000:  # Rotate 90
                 # image = pygame.transform.rotate(image, -90)
                 image = pygame.transform.flip(image, flip_x=False, flip_y=True)
            if rotation_gid & 0x80000000:  # Mirror horizontal, WORKING
                image = pygame.transform.flip(image, flip_x=True, flip_y=False)
            self.images_by_gid[gid] = image


    def dump(self):
        print(f"tmx json file is: {self.filename}")
        print(f"width: {self.width}, height:{self.height}")
        print(f"There are {len(self.images_by_filename)} tile images loaded")
        print(f"There are {len(self.layers)} layers loaded")

    def render_layer(self,
             layer_name,
             target_surface):
        # render the ground layer by iterating through all the tiles
        i = 0
        j = 0
        layer = self.layers[layer_name]
        map_width = self.width
        tile_width, tile_height = 64, 64
        for gid in layer.tiles:
            if gid != 0:
                img = self.images_by_gid[gid]
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
    tiled_map = TiledMap("./maps/test_level.json", 0, 0)
    tiled_map.dump()
    running = True
    frame_num = 0

    # do a test render and see if it shows up correctly
    tiled_map.render_layer("ground", screen)
    tiled_map.render_layer("walls", screen)
    # tiled_map.render_layer("test", screen)  ## This really helped out!!!

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()

        pygame.time.delay(100)

def test3():
    """ test of our own json map reader"""
    pygame.init()
    screen = pygame.display.set_mode((1280,1024))

    # load the tile map
    tiled_map = TiledMap("./maps/forest_glade_v1.json", 0, 0)
    tiled_map.dump()
    running = True
    frame_num = 0

    # do a test render and see if it shows up correctly
    tiled_map.render_layer("ground", screen)
    tiled_map.render_layer("trees", screen)
    tiled_map.render_layer("plants", screen)
    tiled_map.render_layer("items", screen)
    # tiled_map.render_layer("test", screen)  ## This really helped out!!!

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()

        pygame.time.delay(100)


if __name__ == "__main__":
    test3()
