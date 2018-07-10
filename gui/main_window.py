from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QIcon

from .game_frame import GameFrame

import math, time
from time import sleep

class App(QMainWindow):
    def __init__(self, config, optimizers, fastmode=False, fastmode_runs=0, parent=None):
        super(App, self).__init__(parent=parent)
        self.config = config
        self.fastmode = fastmode
        self.fastmode_runs = fastmode_runs
        self.optimizers = optimizers
        self.global_config = self.config.global_config
        self.padding = (200, 200)
        self.resolution = (self.global_config['window']['width'],
                           self.global_config['window']['height'])
        self.window_title = "Evolutionary Game"

        self.debug = {}
        self.init_debug()

        self.initUI()

        # if we have fastmode - run the game for the given amount
        # if self.fastmode:
        #     results = []
        #     for i in range(self.fastmode_runs):
        #         print("run", i+1, "of", self.fastmode_runs)
        #         game_frame = GameFrame(self)
        #         game_frame.start()
        #         #TODO: collect results
        #         # while game_frame.check_game_terminated:
        #         #     sleep(1)
        #         # results.append(game_frame.get_result())
        #     print(results)

    def init_debug(self):
        """
        Declare variables for the Options->Debug
        """
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
        """
        Initialize the graphical user interface
        """
        self.setWindowTitle(self.window_title)
        self.setGeometry(self.padding[0],
                         self.padding[1],
                         self.resolution[0],
                         self.resolution[1])
        self.game_frame = GameFrame(self)
        self.setCentralWidget(self.game_frame)

        # add top menu bar with items
        self.mainMenu = self.menuBar()
        self.gameMenu = self.mainMenu.addMenu('Game')
        self.optionMenu = self.mainMenu.addMenu('Options')
        self.add_option_menu_items()
        self.add_main_menu_items()

        self.statusbar = self.statusBar()

        # connect statusbar with messages from game_frame
        self.game_frame.msg2Statusbar[str].connect(self.statusbar.showMessage)



    def add_main_menu_items(self):
        """
        add all Game menu items (Start Game and Exit)
        """
        self.startButton = QAction('Start Game', self)
        self.startButton.triggered.connect(lambda: self.start_game())
        self.exitButton = QAction('Exit', self)
        self.exitButton.triggered.connect(self.close)

        self.gameMenu.addAction(self.startButton)
        self.gameMenu.addAction(self.exitButton)


    def start_game(self):
        """
        start the game (create a new game instance)
        """
        # enable the statistic button in the top menu bar
        self.statistic_button.setEnabled(True)
        self.game_frame.start()


    def add_option_menu_items(self):
        """
        add items to Option Element in top menu bar
        """
        # create a submenu
        self.toggleMenu = self.optionMenu.addMenu("Debug")
        self.add_toggle_menu_items()
        self.add_statistics_menu()


    def add_statistics_menu(self):
        """
        add item to Option->Show popukation statistics
        """
        self.statistic_button = QAction("show population statistics", self)
        self.statistic_button.triggered.connect(lambda: self.game_frame.open_statistics())
        self.optionMenu.addAction(self.statistic_button)
        # disabled by default
        self.statistic_button.setEnabled(False)


    def add_toggle_menu_items(self):
        """
        add all menu entries for Options->Debug
        """
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
        """
        add button to given menu item and register toggle_debug with the given setting to it
        """
        button = QAction(label, self)
        button.triggered.connect(lambda: self.toggle_debug(setting))
        parent.addAction(button)


    def toggle_debug(self, setting):
        """
        toggle a debug setting
        """
        print("toggle " + setting)
        if setting == "all_perceptions":
            self.debug["all_perceptions"] = not self.debug["all_perceptions"]
            for k, _ in self.debug.items():
                self.debug[k] = self.debug["all_perceptions"]
        else:
            self.debug[setting] = not self.debug[setting]
