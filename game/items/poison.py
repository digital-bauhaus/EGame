from game.items.game_item import GameItem
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import QPoint


class Poison(GameItem):
    def __init__(self, parent, boundary, position=None):
        GameItem.__init__(self, parent, boundary, position)
        self.poison_config = self.items_config["poison"]
        self.size = self.poison_config['size']
        self.color = self.poison_config['color']
        self.nutrition = self.poison_config['poisonness']

    def draw(self, painter):
        color = QColor(self.color)
        painter.setBrush(color)
        painter.setPen(QColor(0,0,0))
        painter.drawRect(self._position[0]-self.size/2,
                         self._position[1]-self.size/2,
                         self.size,
                         self.size)
