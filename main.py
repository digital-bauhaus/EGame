#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from gui.main_window import App
from config import Config
import sys
if __name__ == "__main__":
    config_path = "config.json"
    config = Config(config_path)
    app = QApplication(sys.argv)
    GUI = App(config)
    GUI.show()
    sys.exit(app.exec_())
