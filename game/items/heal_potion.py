from game.items.game_item import GameItem
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen, QPolygonF
from PyQt5.QtCore import QPointF

class HealPotion(GameItem):
    def __init__(self, parent, boundary, position=None):
        GameItem.__init__(self, parent, boundary, position)
        self.health_potion_config = self.items_config['heal_potion']
        self.size = self.health_potion_config['size']
        self.color = self.health_potion_config['color']

    def draw(self, painter):
        color = QColor(self.color)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(color)

        r = self.size/2

        polygon = QPolygonF()
        polygon.append(QPointF(self._position[0] + r, self._position[1] + r/2))
        polygon.append(QPointF(self._position[0]    , self._position[1] + r  ))
        polygon.append(QPointF(self._position[0] - r, self._position[1] + r/2))
        polygon.append(QPointF(self._position[0] - r, self._position[1] - r/2))
        polygon.append(QPointF(self._position[0]    , self._position[1] - r  ))
        polygon.append(QPointF(self._position[0] + r, self._position[1] - r/2))

        painter.drawPolygon(polygon)
