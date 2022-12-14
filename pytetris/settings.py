import pygame as pg

PIECES = ["I", "T", "S", "Z", "L", "J", "O"]

SHAPES = {
    "T": {
        "color": (127, 0, 127),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((0, 1), (1, 1), (2, 1), (1, 0)),
            1: ((0, 1), (1, 1), (1, 2), (1, 0)),
            2: ((0, 1), (1, 1), (2, 1), (1, 2)),
            3: ((1, 1), (2, 1), (1, 2), (1, 0))
        }
    },
    "I": {
        "color": (0, 255, 255),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((0, 0), (1, 0), (2, 0), (3, 0)),
            1: ((2, 2), (2, 1), (2, 0), (2, -1)),
            2: ((0, 1), (1, 1), (2, 1), (3, 1)),
            3: ((1, 2), (1, 1), (1, 0), (1, -1)),
        }
    },
    "S": {
        "color": (0, 255, 0),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((1, 0), (2, 0), (0, 1), (1, 1)),
            1: ((0, 0), (0, 1), (1, 1), (1, 2)),
            2: ((0, 2), (1, 2), (1, 1), (2, 1)),
            3: ((1, 0), (1, 1), (2, 1), (2, 2)),
        }
    },
    "Z": {
        "color": (255, 0, 0),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((0, 0), (1, 0), (1, 1), (2, 1)),
            1: ((1, 0), (1, 1), (0, 1), (0, 2)),
            2: ((0, 1), (1, 1), (1, 2), (2, 2)),
            3: ((2, 0), (2, 1), (1, 1), (1, 2)),
        }
    },
    "O": {
        "color": (255, 255, 0),
        "x_offset": 4,
        "y_offset": -2,
        "rot": {
            0: ((0, 0), (0, 1), (1, 0), (1, 1)),
            1: ((0, 0), (0, 1), (1, 0), (1, 1)),
            2: ((0, 0), (0, 1), (1, 0), (1, 1)),
            3: ((0, 0), (0, 1), (1, 0), (1, 1)),
        }
    },
    "L": {
        "color": (255, 127, 0),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((0, 1), (1, 1), (2, 1), (2, 0)),
            1: ((0, 0), (1, 0), (1, 1), (1, 2)),
            2: ((0, 1), (1, 1), (2, 1), (0, 2)),
            3: ((1, 0), (1, 1), (1, 2), (2, 2)),
        }
    },
    "J": {
        "color": (0, 0, 255),
        "x_offset": 3,
        "y_offset": -2,
        "rot": {
            0: ((0, 0), (0, 1), (1, 1), (2, 1)),
            1: ((1, 0), (1, 1), (1, 2), (0, 2)),
            2: ((0, 1), (1, 1), (2, 1), (2, 2)),
            3: ((1, 0), (2, 0), (1, 1), (1, 2)),
        }
    }
}
WIN_W = 960
WIN_H = 1005
WINDOW_SIZE = (WIN_W, WIN_H)

PLAY_W = 400
PLAY_H = 800
PLAY_SIZE = (PLAY_W, PLAY_H)

GRID_W = 10
GRID_H = 20
GRID_SIZE = (GRID_W, GRID_H)

PLAY_W_OFF = (WIN_W - PLAY_W)//2
PLAY_H_OFF = 200

BOX = PLAY_W // GRID_W

HOLD_X = 40
HOLD_Y = 160

FONT = "NotoSans-Regular.ttf"

SCORE = 0
SCORE_MULT = {1: 100, 2: 300, 3: 600, 4: 1000}

DROP = pg.USEREVENT + 1
PIECE_STOP = pg.USEREVENT + 2
