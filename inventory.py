from ursina import *


class Item(Entity):
    def __init__(self, texture, index):
        super().__init__(
            parent=camera.ui,
            model="quad",
            texture=texture,
            scale=(0.08, 0.08),
            position=(-0.85 + index * 0.09, -0.45),
            color=color.white,
        )
        self.name = texture


class Inventory:
    def __init__(self):
        self.items = []

    def add(self, texture_name):
        if texture_name in [item.name for item in self.items]:
            return
        item = Item(texture=texture_name, index=len(self.items))
        self.items.append(item)

    def have(self, name):
        return any([name == item.name for item in self.items])
