from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QFrame
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QBasicTimer, QPointF, QRectF, QSizeF, pyqtSignal

from game.egame import EGame
from gui.statistics_window import StatisticsWindow

class Board(QFrame):

    msg2Statusbar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.config = parent.config
        self.global_config = parent.global_config
        self.board_dimension = (self.global_config['frame']['width'],
                                self.global_config['frame']['height'])
        self.game_speed = self.global_config['game_speed']
        self.initBoard()
        # self.setMouseTracking(True)
        self.setFixedSize(self.board_dimension[0],
                          self.board_dimension[1])
        self.setStyleSheet("background-color: " + \
            self.global_config['frame']['background_color'])


    # def mouseMoveEvent(self, event):
    #     self.mouse_x = event.x()
    #     self.mouse_y = event.y()

    def open_statistics(self):
        self.statistics_window = StatisticsWindow(self, self.game)


    def refresh_statistic_window(self):
        self.statistics_window.reload(self.game)

    def initBoard(self):
        self.timer = QBasicTimer()
        self.isStarted = False
        self.isPaused = False


    def start(self):
        if self.isPaused:
            return
        print("start game")
        self.game = EGame(self)
        self.game.start()
        self.timer.start(self.game_speed, self)
        self.msg2Statusbar.emit(str("new game started"))
        self.isStarted = True
        if (
            hasattr(self, "statistics_window") 
            and self.statistics_window is not None
        ):
            self.refresh_statistic_window()


    def timerEvent(self, event):
        """
        timer event is called by timer.start()
        updates the game environment
        redraws the objects
        """
        if self.isStarted:
            self.game.update()
            self.update()
            


    def paintEvent(self, event):
        """paint the shapes of the game"""
        painter = QPainter(self)
        if self.isStarted:
            self.game.draw(painter)
