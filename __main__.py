from ursina import *

from map import Map
from settings import Settings
from inventory import Inventory
from chest import Chest
from cabin import Cabin

map = Map()
app = Ursina()
camera.orthographic = True
camera.fov = 10
rows = len(map.map_top_view)
cols = len(map.map_top_view[0])
camera.position = (cols / 2 - 0.5, -rows / 2 + 0.5, -10)
window.color = color.black


class Player(Entity):
    def __init__(self, position):
        super().__init__(
            model="quad",
            color=color.orange,
            position=position,
            scale=0.8 * Settings.TAIL_SIZE,
            collider="box",
        )
        self.inventory = Inventory()
        self.hint_shown = False
        self.cliked_colors = []
        self.chest = Chest((2, 1), (2, 0), position=(3, -2, -0.1))
        self.chest.enabled = False
        self.computer = Entity(
            model="quad",
            texture="computer.png",
            position=(5, -1, -0.1),
            scale=1,
            rotation=(0, 0, 0),
        )
        self.cabin = Cabin((1, -1, -0.1))
        self.computer.enabled = False
        self.cabin.enabled = False

    def input(self, key):
        dx = dy = 0
        match key:
            case "up arrow":
                dy = 1
            case "down arrow":
                dy = -1
            case "left arrow":
                dx = -1
            case "right arrow":
                dx = 1
            case "x":
                if map.room_num == 1:
                    if self.position.x == 1 and self.position.y == -3:
                        # print_on_screen("you click it red")
                        self.add_color("R")
                    elif self.position.x == 2 and self.position.y == -3:
                        # print_on_screen("you click it blue")
                        self.add_color("B")
                    elif self.position.x == 3 and self.position.y == -3:
                        # print_on_screen("you click it green")
                        self.add_color("G")
                    elif self.position.x == 4 and self.position.y == -3:
                        # print_on_screen("you click it purple")
                        self.add_color("P")
                    elif self.position.x == 5 and self.position.y == -3:
                        # print_on_screen("you click it yellow")
                        self.add_color("Y")
                elif map.room_num == 2:
                    if self.position.x == 1 and self.position.y == -1:
                        self.show_msg("this is the cabin")
                        cabin.open()
                    elif self.position.x == 5 and self.position.y == -1:
                        self.computer.enabled = False
                        self.cabin.enabled = False
                        map.load_room(map.room3, 3)
                        self.show_msg("this is the computer")
                        self.input_field = InputField(
                            default_value="",
                            limit_content_to="abcdefghijklmnopqrstuvwxyz",
                            position=(0, 0),
                            scale=(0.5, 0.1),
                            active=True,
                        )

                        def handel_submit():
                            if self.input_field.text == "access":
                                destroy(self.input_field)
                                map.load_room(Map.room2, 2)

                                self.computer.enabled = True
                                self.cabin.enabled = True
                                self.cabin.open()
                                self.inventory.add("card_key.png")
                                self.button.enabled = False

                        self.button = Button(
                            text="Submit",
                            position=(0, -0.2),
                            scale=(0.2, 0.1),
                            on_click=handel_submit,
                        )

                        self.show_msg(
                            "ENTER PASSWORD: (Hint scrambled letters: ssccea)"
                        )

        new_x = int(self.x + dx)
        new_y = int(self.y + dy)

        row = -new_y
        col = new_x

        if 0 <= row < len(map.map_top_view) and 0 <= col < len(map.map_top_view[0]):
            if not self.hint_shown and map.room_num == 1:
                if self.y == -5 and new_y == -4:
                    self.show_msg(
                        "Try stepping on the tiles starting with the cool colors before the warm ones.",
                    )
                    self.hint_shown = True
            tile = map.map_top_view[row][col]
            if tile not in ["&", "%"]:
                self.position = (new_x, new_y, -0.1)

            if tile == "%":
                if map.room_num == 1 and self.inventory.have("key.png"):
                    self.position = (3, -5, -0.1)
                    destroy(self.chest)
                    self.cabin.enabled = True
                    self.computer.enabled = True
                    map.load_room(map.room2, 2)

                elif map.room_num == 2 and self.inventory.have("card_key.png"):
                    self.show_msg("You won")

    def add_color(self, key):
        correct_color_list = ["B", "G", "Y", "R", "P"]
        if correct_color_list[len(self.cliked_colors)] == key:
            self.cliked_colors.append(key)
        else:
            self.cliked_colors = []
            self.show_msg("Wrong Start again")

        if len(self.cliked_colors) == 5:
            self.cliked_colors = []
            self.inventory.add("key.png")
            self.chest.enabled = True
            self.chest.scale = 0
            self.chest.animate_scale(1.5, duration=0.3, curve=curve.out_elastic)
            invoke(self.chest.open, delay=0.3)

    def show_msg(self, msg):
        print_on_screen(
            msg,
            position=(0, 0.4),
            duration=3,
        )


player = Player((3, -5, -0.1))
# player.inventory.add("key.png")
# player.inventory.add("another-key")
app.run()
