from game.items.game_item import GameItem
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QPolygonF
from PyQt5.QtCore import QPointF

class Corpse(GameItem):
    def __init__(self, parent, boundary, poison, position):
        GameItem.__init__(self, parent, boundary, position)
        self.corpse_config = self.items_config['corpse']
        self.size = self.corpse_config['size']
        self.color = self.corpse_config['color']
        self.nutrition = self.corpse_config['nutrition']
        self.poison = poison

    def draw(self, painter):
        color = QColor(self.color)
        painter.setBrush(color)

        r = self.size/2

        polygon = QPolygonF()
        polygon.append(QPointF(self._position[0] + r, self._position[1] + r/2))
        polygon.append(QPointF(self._position[0], self._position[1] + r))
        polygon.append(QPointF(self._position[0] - r, self._position[1] + r/2))
        polygon.append(QPointF(self._position[0] - r, self._position[1] - r/2))
        polygon.append(QPointF(self._position[0], self._position[1] - r))
        polygon.append(QPointF(self._position[0] + r, self._position[1] - r/2))

        painter.drawPolygon(polygon)
