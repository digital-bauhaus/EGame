from PyQt5.QtWidgets import QMainWindow, QFrame, QAction, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QFileDialog, QComboBox, QLabel, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .game_frame import GameFrame

import importlib.util
import os
import math, time
from time import sleep

class App(QMainWindow):
    def __init__(self, config, fastmode=False, fastmode_runs=0, parent=None):
        super(App, self).__init__(parent=parent)
        self.toggleDebug = False
        self.selectedBreederBlue = False
        self.selectedBreederYellow = False
        self.config = config
        self.fastmode = fastmode
        self.fastmode_runs = fastmode_runs
        self.gameModes = ['Normal', 'Beach', 'Street', 'Magma', 'Terrace', 'Snow']
        self.selectedMode = 'normal'

        #self.optimizers = optimizers
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
        # disable so they won't show in the main menu
        self.gameMenu.setEnabled(False)
        self.optionMenu.setEnabled(False)
        self.mainMenu.setVisible(False)


        self.statusbar = self.statusBar()


    def init_main_frame(self):
        """
        Initialize the Main Menu (start screen)
        """
        self.main_frame = QFrame(self)

        
        self.main_frame.setStyleSheet("background-color: rgb(126, 144, 173)")

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame.resize(self.width(), self.height())

        self.verticalLayoutWidget = QWidget(self.main_frame)
        self.verticalLayoutWidget.resize(self.width(), self.height())
        
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
    
        self.pushButton = QPushButton("Play New Game", self.verticalLayoutWidget)
        self.pushButton.setFlat(True)
        self.pushButton.setStyleSheet("color: white; font-weight: bold;font-size: 36px; font-family: Helvetica, sans-serif;")
        
        self.pushButton.clicked.connect(self.handlePlayButtonMainMenu)
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton("Options",self.verticalLayoutWidget)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.pushButton_3.clicked.connect(self.handleOptionsButton)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton("Quit", self.verticalLayoutWidget)
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
        self.opt_frame.resize(self.width(), self.height())

        self.vertLayoutW = QWidget(self.opt_frame)
        self.vertLayoutW.resize(self.width(), self.height())

        self.vertLayout = QVBoxLayout(self.vertLayoutW)
        self.vertLayout.setContentsMargins(0, 0, 0, 0)
        self.vertLayout.setAlignment(Qt.AlignCenter)

        self.backButton = QPushButton("Back", self.vertLayoutW)
        self.backButton.setFlat(True)
        self.backButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")

        self.backButton.clicked.connect(self.backButtonPressed)
        self.backButton.resize(self.backButton.minimumSizeHint())

        self.checkBox = QCheckBox("Show Debug options", self.vertLayoutW)
        self.checkBox.toggled.connect(self.toggleOptions)
        
        if self.toggleDebug == True:
            self.checkBox.setChecked(True)

        self.checkBox.setStyleSheet("QCheckBox{ color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;} QCheckBox::indicator { width: 25px; height: 25px;};")    
        self.vertLayout.addWidget(self.checkBox, 0, Qt.AlignCenter)
        self.vertLayout.addWidget(self.backButton, 0, Qt.AlignCenter)

   

    def init_pregame(self):
        """
        screen before a game is played, let's you select a game mode and a breeder.py file
        """
        self.pregame_frame = QFrame(self)
        self.pregame_frame.setStyleSheet("background-color: rgb(126, 144, 173)")

        self.pregame_frame.setFrameShape(QFrame.StyledPanel)
        self.pregame_frame.setFrameShadow(QFrame.Raised)
        self.pregame_frame.resize(self.width(), self.height())

        self.preVertLayoutW = QWidget(self.pregame_frame)
        self.preVertLayoutW.resize(self.width(), self.height())

        self.preVertLayout = QVBoxLayout(self.preVertLayoutW)
        self.preVertLayout.setContentsMargins(0, 0, 0, 0)
        self.preVertLayout.setAlignment(Qt.AlignCenter)

        self.selectorButton = QPushButton("Click to select the breeder class for Blue", self.preVertLayoutW)
        self.selectorButton.setFlat(True)
        self.selectorButton.setStyleSheet("color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;")
        self.selectorButton.clicked.connect(self.select_breeder_blue)

        self.selector2Button = QPushButton("Click to select the breeder class for Yellow", self.preVertLayoutW)
        self.selector2Button.setFlat(True)
        self.selector2Button.setStyleSheet("color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;")
        self.selector2Button.clicked.connect(self.select_breeder_yellow)

        self.modeText = QLabel(self.preVertLayoutW)
        self.modeText.setText("Game mode:")
        self.modeText.setStyleSheet("color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;")

        self.modeSelect = QComboBox(self.preVertLayoutW)
        for mode in self.gameModes:
            self.modeSelect.addItem(mode)

        self.modeSelect.setStyleSheet("color: white; font-weight: bold; font-size: 30px; font-family: Helvetica, sans-serif;")
        self.modeSelect.currentIndexChanged.connect(self.mode_select)
        
        self.preHorizontalLayoutW = QWidget(self.pregame_frame)

        self.preHorizontalLayout = QHBoxLayout(self.preHorizontalLayoutW)
        self.preHorizontalLayout.setAlignment(Qt.AlignBottom)

        self.playButton = QPushButton("Play", self.preHorizontalLayoutW)
        self.playButton.setFlat(True)
        self.playButton.setStyleSheet("color: rgb(211,211,211); font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.playButton.clicked.connect(self.handlePlayButton)

        self.preBackButton = QPushButton("Back", self.preHorizontalLayoutW)
        self.preBackButton.setFlat(True)
        self.preBackButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.preBackButton.clicked.connect(self.backButtonPressed)
     
        self.preHorizontalLayout.addWidget(self.preBackButton)
        self.preHorizontalLayout.addWidget(self.playButton)

        self.preVertLayout.addWidget(self.selectorButton)
        self.preVertLayout.addWidget(self.selector2Button)
        self.preVertLayout.addWidget(self.modeText)
        self.preVertLayout.addWidget(self.modeSelect)
        self.preVertLayout.addWidget(self.preHorizontalLayoutW)

        # only press play when a breeder is selected
        self.playButton.setEnabled(False)


    def init_gameover_frame(self, winner=None):
        """
        screen when a game is done
        """
        self.gameover_frame = QFrame(self)
        self.gameover_frame.setStyleSheet("background-color: rgb(126, 144, 173)")

        self.gameover_frame.setFrameShape(QFrame.StyledPanel)
        self.gameover_frame.setFrameShadow(QFrame.Raised)
        self.gameover_frame.resize(self.width(), self.height())

        self.overVertLayoutW = QWidget(self.gameover_frame)
        self.overVertLayoutW.resize(self.width(), self.height())

        self.overVertLayout = QVBoxLayout(self.overVertLayoutW)
        self.overVertLayout.setContentsMargins(0, 0, 0, 0)
        self.overVertLayout.setAlignment(Qt.AlignCenter)

        self.gameOverText = QLabel(self.overVertLayoutW)
        self.gameOverText.setText("Game over. " + winner + " won!")
        self.gameOverText.setStyleSheet("color: white; font-weight: bold; font-size: 46px; font-family: Helvetica, sans-serif;")

        self.overHorizontalLayoutW = QWidget(self.gameover_frame)

        self.overHorizontalLayout = QHBoxLayout(self.overHorizontalLayoutW)
        self.overHorizontalLayout.setAlignment(Qt.AlignBottom)

        self.playAgainButton = QPushButton("New Game", self.overHorizontalLayoutW)
        self.playAgainButton.setFlat(True)
        self.playAgainButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.playAgainButton.clicked.connect(self.handlePlayButtonMainMenu)

        self.backToMMButton = QPushButton("Back", self.overHorizontalLayoutW)
        self.backToMMButton.setFlat(True)
        self.backToMMButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.backToMMButton.clicked.connect(self.backToMenuButton)

        self.quitGameButton = QPushButton("Quit", self.overHorizontalLayoutW)
        self.quitGameButton.setFlat(True)
        self.quitGameButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
        self.quitGameButton.clicked.connect(self.handleExitButton)


        self.overHorizontalLayout.addWidget(self.playAgainButton)
        self.overHorizontalLayout.addWidget(self.backToMMButton)
        self.overHorizontalLayout.addWidget(self.quitGameButton)

        self.overVertLayout.addWidget(self.gameOverText)
        self.overVertLayout.addWidget(self.overHorizontalLayoutW)


    def play_game(self):
        """
        starts a new game
        """
        #Enable top menu and status bar
        self.statusbar.setVisible(True)
        self.mainMenu.setVisible(True)
        self.gameMenu.setEnabled(True)
        self.optionMenu.setEnabled(True)
        
        self.selectedBreederBlue = False
        self.selectedBreederYellow = False
        # check whether debug settings were enabled in the options menu
        if self.toggleDebug == True:
            self.toggleMenu.setEnabled(True)
        else:
            self.toggleMenu.setEnabled(False)
        
        self.game_frame = GameFrame(self, self.selectedMode, self.width(), self.height())
        self.setCentralWidget(self.game_frame)

        # connect statusbar with messages from game_frame
        self.game_frame.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.start_game()


    def start_game(self):
        """
        start the game (create a new game instance)
        """
        # enable the statistic button in the top menu bar
        self.statistic_button.setEnabled(True)
        self.game_frame.start()


    def game_over(self, winner):
        """
        Game is finished (this method is called from egame.py)
        """
        self.init_gameover_frame(winner)
        self.setCentralWidget(self.gameover_frame)
        self.statusbar.setVisible(False)
        self.show()


    def handlePlayButtonMainMenu(self):
        """
        Play is pressed in the main menu
        """
        self.init_pregame()
        self.setCentralWidget(self.pregame_frame)
        self.show()


    def handlePlayButton(self):
        """
        Play is pressed in pre game menu
        """
        self.statusbar.setVisible(True)
        self.play_game()


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
        if self.checkBox.isChecked() == True:
            self.toggleDebug = True
        else:
            self.toggleDebug = False


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
        self.gameMenu.setEnabled(False)
        self.optionMenu.setEnabled(False)
        self.setCentralWidget(self.main_frame)
        self.verticalLayoutWidget.resize(self.width(), self.height())
        self.show()


    def mode_select(self, index):
        """
        A mode in the pregame screen was selected, change game mode
        """
        self.selectedMode = self.modeSelect.currentText().lower()


    def select_breeder_blue(self):
        """
        File selector dialog to open a breeder class
        """
        self.breederBluePath = QFileDialog.getOpenFileName(None, 'Select breeder class', self.config.global_config["breeder_directory"], "Python files (*.py)")

        if self.breederBluePath != '':
            self.selectedBreederBlue = True
            self.breederBluePath = self.breederBluePath[0]
            self.check_selection()
        
    
    def select_breeder_yellow(self):
        """"
        File selector dialog to open a second breeder class
        """
        self.breederYellowPath = QFileDialog.getOpenFileName(None, 'Select breeder class', self.config.global_config["breeder_directory"], "Python files (*.py)")
        
        if self.breederYellowPath != '':
            self.selectedBreederYellow = True
            self.breederYellowPath = self.breederYellowPath[0]
            self.check_selection()

            
    def resizeEvent(self, event):
        """
        Window size has changed, resize frames accordingly 
        BUG: It sometimes throws a Runtime Error because the garbage collector of PyQT has deleted a frame. It still works though.  
        """   
        try:    
            if hasattr(self, 'main_frame') and self.main_frame is not None:
                self.main_frame.resize(self.width(), self.height())
                if hasattr(self, 'verticalLayoutWidget') and self.verticalLayoutWidget is not None:
                    self.verticalLayoutWidget.resize(self.width(), self.height())
            
            if hasattr(self, 'pregame_frame') and self.pregame_frame is not None:
                self.pregame_frame.resize(self.width(), self.height())
                if hasattr(self, 'preVertLayoutW') and self.preVertLayoutW is not None:
                    self.preVertLayoutW.resize(self.width(), self.height())
                    print("resizing preVertLayoutW")

            if hasattr(self, 'opt_frame') and self.opt_frame is not None:    
                self.opt_frame.resize(self.width(), self.height())
                if hasattr(self, 'vertLayoutW') and self.vertLayoutW is not None:
                    self.vertLayoutW.resize(self.width(), self.height())

            if hasattr(self, 'game_frame') and self.game_frame is not None:        
                self.game_frame.resize_frame(self.width(), self.height())
            
            if hasattr(self, 'gameover_frame') and self.gameover_frame is not None:
                self.gameover_frame.resize(self.width(), self.height())
                if hasattr(self, 'overVertLayoutW') and self.overVertLayoutW is not None:
                    self.overVertLayoutW.resize(self.width(), self.height())
        # not so nice workaround for the bug stated above 
        except RuntimeError:
            pass

    
    def keyPressEvent(self, event):
        """
        F11 = fullscreen, Esc = back to normal size window
        """
        if event.key() == Qt.Key_Escape:
            self.showNormal()
        if event.key() == Qt.Key_F11:
            self.showFullScreen()
    
    
    def check_selection(self):
        """
        checks if two files were selected, if yes, load the classes and enable the play button
        """
        if self.selectedBreederBlue == True and self.selectedBreederYellow == True:
            self.playButton.setStyleSheet("color: white; font-weight: bold; font-size: 36px; font-family: Helvetica, sans-serif;")
            self.playButton.setEnabled(True)        
            self.optimizers = self.load_breeders(self.breederBluePath, self.breederYellowPath)


    def load_breeders(self, path1, path2):
        """
        Loades breeder classes (this code was previously in main.py)
        """
        spec1 = importlib.util.spec_from_file_location("opti1", path1)
        spec2 = importlib.util.spec_from_file_location("opti2", path2)
        module1 = importlib.util.module_from_spec(spec1)
        module2 = importlib.util.module_from_spec(spec2)
        spec1.loader.exec_module(module1)
        spec2.loader.exec_module(module2)
        return [module1, module2]

    
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


    def add_option_menu_items(self):
        """
        add items to Option Element in top menu bar
        """
        # create a submenu
        self.toggleMenu = self.optionMenu.addMenu("Debug")
        self.toggleMenu.setStatusTip("Can be enabled in the settings")
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
