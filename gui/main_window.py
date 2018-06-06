from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QIcon

from .frame import Board

import math

class App(QMainWindow):


    def __init__(self, config, parent=None):
        super(App, self).__init__(parent=parent)
        self.config = config
        self.global_config = self.config.global_config
        self.padding = (200, 200)
        self.resolution = (self.global_config['window']['width'],
                           self.global_config['window']['height'])
        self.window_title = "Evolutionary Game"

        self.debug = {}
        self.init_debug()

        self.initUI()

    def init_debug(self):
        self.debug["repell_frame"] = True
        self.debug["health"] = True
        self.debug["velocity_vector"] = False
        self.debug["food_perception"] = False
        self.debug["poison_perception"] = False
        self.debug["opponent_perception"] = False
        self.debug["predator_perception"] = False
        self.debug["potion_perception"] = False
        self.debug["corpse_perception"] = False
        self.debug["all_perceptions"] = False

    def initUI(self):
        self.setWindowTitle(self.window_title)
        self.setGeometry(self.padding[0],
                         self.padding[1],
                         self.resolution[0],
                         self.resolution[1])
        self.game_widget = Board(self)
        self.setCentralWidget(self.game_widget)

        self.mainMenu = self.menuBar()
        self.gameMenu = self.mainMenu.addMenu('Game')
        self.optionMenu = self.mainMenu.addMenu('Options')
        self.add_option_menu_items()
        self.add_main_menu_items()

        self.statusbar = self.statusBar()
        self.game_widget.msg2Statusbar[str].connect(self.statusbar.showMessage)



    def add_main_menu_items(self):
        self.startButton = QAction('Start Game', self)
        self.startButton.triggered.connect(lambda: self.start_game())
        self.exitButton = QAction('Exit', self)
        self.exitButton.triggered.connect(self.close)

        self.gameMenu.addAction(self.startButton)
        self.gameMenu.addAction(self.exitButton)

    def start_game(self):
        self.statistic_button.setEnabled(True)
        self.game_widget.start()

    def add_option_menu_items(self):
        self.toggleMenu = self.optionMenu.addMenu("Debug")
        self.add_toggle_menu_items()
        self.add_statistics_menu()


    def add_statistics_menu(self):
        self.statistic_button = QAction("show population statistics", self)
        self.statistic_button.triggered.connect(lambda: self.game_widget.open_statistics())
        self.optionMenu.addAction(self.statistic_button)
        self.statistic_button.setEnabled(False)


    def add_toggle_menu_items(self):
        self.build_button(
            self.toggleMenu, 'toggle repell frame', "repell_frame")
        self.build_button(
            self.toggleMenu, 'toggle health display', "health")
        self.build_button(
            self.toggleMenu, 'toggle velocity vector', "velocity_vector")
        self.build_button(
            self.toggleMenu, 'toggle food perception radius', "food_perception")
        self.build_button(
            self.toggleMenu, 'toggle poison perception radius', "poison_perception")
        self.build_button(
            self.toggleMenu, 'toggle opponent perception radius', "opponent_perception")
        self.build_button(
            self.toggleMenu, 'toggle predator perception radius', "predator_perception")
        self.build_button(
            self.toggleMenu, 'toggle potion perception radius', "potion_perception")
        self.build_button(
            self.toggleMenu, 'toggle corpse perception radius', "corpse_perception")
        self.build_button(
            self.toggleMenu, 'toggle all perception radius', "all_perceptions")

    def build_button(self, parent, label, setting):
        button = QAction(label, self)
        button.triggered.connect(lambda: self.toggle_debug(setting))
        parent.addAction(button)


    def toggle_debug(self, setting):
        print("toggle " + setting)
        if setting == "all_perceptions":
            self.debug["all_perceptions"] = not self.debug["all_perceptions"]
            for k, _ in self.debug.items():
                self.debug[k] = self.debug["all_perceptions"]
        else:
            self.debug[setting] = not self.debug[setting]
        # self.print_settings()

    def print_settings(self):
        for key, value in self.debug.items():
            print(key, "\t", value)
