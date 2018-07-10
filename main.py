#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import App
from fastmode import Fastmode
from config import Config
import sys
import importlib.util
if __name__ == "__main__":

    # program parameter:
    # config.path optimizer1 optimizer2

    if len(sys.argv) < 4:
        print("Wrong number of parameter! call: python3 ./main.py /path/to/config.json /path/to/optimizer1 /path/to/optimizer2")
        sys.exit(0)
    config_path = sys.argv[1]
    config = Config(config_path)
    optimizer1_path = sys.argv[2]
    optimizer2_path = sys.argv[3]
    spec1 = importlib.util.spec_from_file_location("opti1", optimizer1_path)
    spec2 = importlib.util.spec_from_file_location("opti2", optimizer2_path)
    module1 = importlib.util.module_from_spec(spec1)
    module2 = importlib.util.module_from_spec(spec2)
    spec1.loader.exec_module(module1)
    spec2.loader.exec_module(module2)

    # fast mode additional parameter: bool enabled, int runs
    fastmode = False
    fastmode_runs = 0
    if len(sys.argv) > 4:
        fastmode = sys.argv[4]
        fastmode_runs = int(sys.argv[5])
        
        fastmode_instance = Fastmode(config, [module1, module2], fastmode_runs)
        fastmode_instance.run()

    else:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('./img/game_icon3.png'))
        GUI = App(config, [module1, module2], fastmode, fastmode_runs)
        GUI.show()
        sys.exit(app.exec_())
