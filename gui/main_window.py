from PyQt5.QtWidgets import QMainWindow, QFrame, QAction, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .game_frame import GameFrame

import math, time
from time import sleep

class App(QMainWindow):
    def __init__(self, config, optimizers, fastmode=False, fastmode_runs=0, parent=None):
        super(App, self).__init__(parent=parent)
        self.toggleDebug = False
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

        self.init_main_frame()

        # add top menu bar with items
        self.mainMenu = self.menuBar()
        self.gameMenu = self.mainMenu.addMenu('Game')
        self.optionMenu = self.mainMenu.addMenu('Options')
        self.add_option_menu_items()
        self.add_main_menu_items()

        self.gameMenu.setEnabled(False)
        self.optionMenu.setEnabled(False)



        self.statusbar = self.statusBar()


    def init_main_frame(self):
        """
        Initialize the Main Menu (start screen)
        """
        self.main_frame = QFrame(self)

        self.main_frame.setStyleSheet("background-color: rgb(126, 144, 173)")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame.resize(800,600)

        self.verticalLayoutWidget = QWidget(self.main_frame)
        self.verticalLayoutWidget.resize(800,600)
        
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
    
        self.pushButton = QPushButton("Play", self.verticalLayoutWidget)
        self.pushButton.setFlat(True)
        self.pushButton.setStyleSheet("color: white; font-weight: bold;font-size: 36px; font-family: Helvetica, sans-serif;")
        self.pushButton.clicked.connect(self.handlePlayButton)

        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QPushButton("Options",self.verticalLayoutWidget)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.pushButton_3.clicked.connect(self.handleOptionsButton)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton("Exit", self.verticalLayoutWidget)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.pushButton_2.clicked.connect(self.handleExitButton)
        self.verticalLayout.addWidget(self.pushButton_2)
    

    def init_options(self):
        """
        Initialize the Options Menu
        """
        self.opt_frame = QFrame(self)
        self.opt_frame.setStyleSheet("background-color: rgb(126, 144, 173)")

        self.opt_frame.setFrameShape(QFrame.StyledPanel)
        self.opt_frame.setFrameShadow(QFrame.Raised)
        self.resize(800,600)

        self.vertLayoutW = QWidget(self.opt_frame)
        self.vertLayoutW.resize(800,600)

        self.vertLayout = QVBoxLayout(self.vertLayoutW)
        self.vertLayout.setContentsMargins(0, 0, 0, 0)
        self.vertLayout.setAlignment(Qt.AlignCenter)

        self.backButton = QPushButton("Back", self.vertLayoutW)
        self.backButton.setFlat(True)
        self.backButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")

        self.backButton.clicked.connect(self.backButtonPressed)
        self.backButton.resize(self.backButton.minimumSizeHint())

        self.radioButton = QRadioButton("Show Debug options", self.vertLayoutW)
        self.radioButton.toggled.connect(self.toggleOptions)
        
        if self.toggleDebug == True:
            self.radioButton.setChecked(True)

        self.radioButton.setStyleSheet("QRadioButton{ color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;} QRadioButton::indicator { width: 25px; height: 25px;};")    
        self.vertLayout.addWidget(self.radioButton, 0, Qt.AlignCenter)
        self.vertLayout.addWidget(self.backButton, 0, Qt.AlignCenter)
   

    def handlePlayButton(self):
        """
       Play is pressed in Main menu
        """
        self.gameMenu.setEnabled(True)
        if self.toggleDebug == True:
            self.optionMenu.setEnabled(True)
        
        self.game_frame = GameFrame(self)
        self.setCentralWidget(self.game_frame)

        # connect statusbar with messages from game_frame
        self.game_frame.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.start_game()
        #self.show()

    def handleOptionsButton(self):
        """
        Options is pressed in main menu
        """
        self.init_options()
        self.setCentralWidget(self.opt_frame)
        self.show()


    def handleExitButton(self):
        """
        Exit button closes the main frame
        """
        self.close()  

    def backButtonPressed(self):
        """
        Back button in options frame
        """
        self.backToMenu()

    def toggleOptions(self):
        """
        Debug toggle button to enable/disable debug settings
        """
        if self.radioButton.isChecked() == True:
            self.toggleDebug = True
        else:
            self.toggleDebug = False

    def resizeEvent(self, event):
        """
        Window size has changed, resize frames accordingly 
        """
        if hasattr(self, 'game_frame') and self.game_frame is not None:
            self.game_frame.resize(self.width(), self.height())
        
        if hasattr(self, 'main_frame') and self.main_frame is not None:
            self.main_frame.resize(self.width(), self.height())
            if hasattr(self, 'verticalLayoutWidget') and self.verticalLayoutWidget is not None:
                self.verticalLayoutWidget.resize(self.width(), self.height())
        
        if hasattr(self, 'opt_frame') and self.opt_frame is not None:    
            self.opt_frame.resize(self.width(), self.height())
            if hasattr(self, 'vertLayoutW') and self.vertLayoutW is not None:
                self.vertLayoutW.resize(self.width(), self.height())
    
    
    def keyPressEvent(self, event):
        """
        F11 = fullscreen, Esc = back to normal size window
        """
        if event.key() == Qt.Key_Escape:
            self.showNormal()
        if event.key() == Qt.Key_F11:
            self.showFullScreen()


    def add_main_menu_items(self):
        """
        add all Game menu items (Start new game, back to main menu and Exit)
        """
        self.startButton = QAction('Restart', self)
        self.startButton.triggered.connect(lambda: self.start_game())
        self.exitButton = QAction('Exit', self)
        self.exitButton.triggered.connect(self.close)
        self.backMenuButton = QAction('Back to Main Menu', self)
        self.backMenuButton.triggered.connect(self.backToMenuButton)

        self.gameMenu.addAction(self.startButton)
        self.gameMenu.addAction(self.backMenuButton)
        self.gameMenu.addAction(self.exitButton)


    def backToMenuButton(self):
        """
        Game is stopped and main menu is shown
        """
        self.game_frame.stop_timer()
        self.backToMenu()


    def backToMenu(self):
        """
        reinitialize main menu screen
        """
        self.init_main_frame()
        self.setCentralWidget(self.main_frame)
        self.verticalLayoutWidget.resize(self.width(), self.height())
        self.show()

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
        add item to Option->Show population statistics
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
