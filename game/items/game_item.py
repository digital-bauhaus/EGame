import numpy as np
from random import randint


class GameItem():
    def __init__(self, parent, boundary, position=None):
        self.parent = parent
        self.config = parent.config
        self.items_config = self.config.items
        if position is None:
            _left_border = boundary
            _right_border = int(self.parent.board_dimension[0]) - boundary
            _top_border = boundary
            _bottom_border = int(self.parent.board_dimension[1]) - boundary
            _x = float(randint(_left_border, _right_border))
            _y = float(randint(_top_border, _bottom_border))
            self._position = np.array([_x, _y])
        else:
            self._position = position