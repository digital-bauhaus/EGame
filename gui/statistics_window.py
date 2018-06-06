from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QBasicTimer
from gui.statistics_widget import StatisticsWidget


class StatisticsWindow(QMainWindow):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.statistics_widget = StatisticsWidget(self, game)
        self.timer = QBasicTimer()
        self.timer.start(20, self)
        self.show()
    
    def update(self):
        self.statistics_widget.update()

    def reload(self, game):
        self.statistics_widget.reload(game)

    def timerEvent(self, event):
        self.update()



