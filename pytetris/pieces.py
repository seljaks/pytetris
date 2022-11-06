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
