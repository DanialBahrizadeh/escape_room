from ursina import *

from settings import Settings


class Tail(Entity):
    def __init__(self, x: int, y: int, symbol):
        super().__init__(
            model="quad",
            color=Map.translator.get(symbol, color.white),
            position=(y, -x, 0),
            scale=Settings.TAIL_SIZE,
            collider="box",
        )
        self.symbol = symbol


class Map:
    room1 = [
        #
        "&&&%&&&",
        "&*****&",
        "&*****&",
        "&RBGPY&",
        "&*****&",
        "&&&*&&&",
    ]

    room2 = [
        #
        "&&&%&&&",
        "&C***T&",
        "&*****&",
        "&*****&",
        "&*****&",
        "&&&*&&&",
    ]

    room3 = [
        #
        "&&&%&&&",
        "&!!!!!&",
        "&!!!!!&",
        "&!!!!!&",
        "&!!!!!&",
        "&&&&&&&",
    ]

    translator = {
        "&": color.gray,
        "*": color.white,
        "%": color.pink,
        "R": color.red,
        "B": color.blue,
        "G": color.green,
        "P": color.violet,
        "Y": color.yellow,
        "T": color.white,
        "C": color.rgba(200, 255, 255, 150),
        "!": color.blue,
    }

    def __init__(self) -> None:
        # self.tails = [
        #     Tail(row, col)
        #     for row in range(len(Map.map_top_view))
        #     for col in range(len(Map.map_top_view[0]))
        # ]
        self.tails = []
        self.map_top_view = []
        self.room_num = 1
        self.load_room(self.room1, 1)

    def load_room(self, room_data, room_num):
        for tile in self.tails:
            destroy(tile)
        self.tails.clear()

        self.map_top_view = room_data
        self.room_num = room_num

        self.tails = [
            Tail(row, col, room_data[row][col])
            for row in range(len(room_data))
            for col in range(len(room_data[0]))
        ]
