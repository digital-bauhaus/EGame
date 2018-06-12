import numpy as np
from random import randint

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QPointF


class GameItem():
    def __init__(self, parent, boundary, position=None):
        self.parent = parent
        self.config = parent.config
        self.items_config = self.config.items
        if position is None:
            _left_border = boundary
            _right_border = int(self.parent.frame_dimension[0]) - boundary
            _top_border = boundary
            _bottom_border = int(self.parent.frame_dimension[1]) - boundary
            _x = float(randint(_left_border, _right_border))
            _y = float(randint(_top_border, _bottom_border))
            self._position = np.array([_x, _y])
        else:
            self._position = position

    def draw_image(self, painter):
        item_image = QImage(self.image)
        painter.drawImage(QPointF(self._position[0]-(item_image.height()/2), 
                                  self._position[1]-(item_image.width()/2)), 
                                  item_image)