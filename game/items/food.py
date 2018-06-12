from game.items.game_item import GameItem
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import QPoint


class Food(GameItem):
    def __init__(self, parent, boundary, position=None):
        GameItem.__init__(self, parent, boundary, position)
        self.food_config = self.items_config["food"]
        self.size = self.food_config['size']
        self.color = self.food_config['color']
        self.image = self.food_config['image']
        self.nutrition = self.food_config['nutrition']
    
    def draw(self, painter):
        if self.image is "":
            self.draw_polygon(painter)
        else:
            self.draw_image(painter)

    def draw_polygon(self, painter):
        color = QColor(self.color)
        painter.setBrush(color)
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(self._position[0]-self.size/2,
                         self._position[1]-self.size/2,
                         self.size,
                         self.size)
