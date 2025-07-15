from ursina import *


class Cabin(Entity):
    def __init__(self, position):
        super().__init__(
            model="quad",
            texture="closed_cabin.png",
            position=position,
            scale=1.5,
        )
        self.is_open = False

    def open(self):
        if self.is_open:
            return

        self.texture = "open_cabin.png"
        self.is_open = True

        self.animate_scale(self.scale * 1.2, duration=0.15, curve=curve.out_quint)
        invoke(self.animate_scale, self.scale, delay=0.15, duration=0.1)
