from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QFrame
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QBasicTimer, QPointF, QRectF, QSizeF, pyqtSignal

from game.egame import EGame
from gui.statistics_window import StatisticsWindow

class GameFrame(QFrame):

    msg2Statusbar = pyqtSignal(str)

    def __init__(self, parent, frame_width=None, frame_height=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = parent.config
        self.global_config = parent.global_config
        if frame_width is None and frame_height is None:
            self.frame_dimension = (self.global_config['frame']['width'],
                                   self.global_config['frame']['height']) 
        else:    
            self.frame_dimension = (frame_width, frame_height)

        if self.parent_window.fastmode:
            self.game_speed = 0
        else:
            self.game_speed = self.global_config['game_speed']
        self.init_frame()
        self.resize(self.frame_dimension[0],
                          self.frame_dimension[1])
        #self.setStyleSheet("background-color: " + \
        #    self.global_config['frame']['background_color'])
        #self.setStyleSheet("background-image: " + \
        #    self.global_config['frame']['background_image'])
        self.setStyleSheet("background-image: " + \
            self.global_config['frame']['background_image'])
                

    def resize_frame(self, width, height):
        """
        resize frame and adjust frame_dimension
        """
        self.resize(width, height)
        self.frame_dimension = (width, height)

    def open_statistics(self):
        """
        open a new window to display population details
        """
        self.statistics_window = StatisticsWindow(self, self.game)


    def refresh_statistic_window(self):
        """
        reload the statistic window with the new game instance
        """
        self.statistics_window.reload(self.game)


    def init_frame(self):
        """
        init the frame and declare frame variables
        """
        self.timer = QBasicTimer()
        self.isStarted = False
        self.isPaused = False


    def start(self):
        """
        start a new EGame
        """
        if self.isPaused:
            return
        print("start game")
        self.game = EGame(self)
        self.game.start()
        self.timer.start(self.game_speed, self)
        self.msg2Statusbar.emit(str("new game started"))
        self.isStarted = True
        # check if there is a statistic window opened
        if (
            hasattr(self, "statistics_window") 
            and self.statistics_window is not None
        ):
            self.refresh_statistic_window()


    def update_frame(self):
        if self.isStarted:
            self.game.update()
        self.update()

    def stop_timer(self):
        self.timer.stop()

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
        # paint only when game is started
        if self.isStarted:
            self.game.draw(painter)
