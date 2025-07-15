from ursina import *


class Chest(Sprite):
    def __init__(self, closed_tile, open_tile, position):
        super().__init__(
            texture="treasure_chests_32x32.png",
            tileset_size=(10, 12),
            tile_coordinate=closed_tile,
            position=position,
            scale=0.3,
        )
        self.closed_tile = closed_tile
        self.open_tile = open_tile
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.tile_coordinate = self.open_tile
            self.is_open = True
            print_on_screen("A hidden chest opens!", position=(0, 0.4), duration=3)
