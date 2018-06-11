#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from gui.main_window import App
from config import Config
import sys
import importlib.util
if __name__ == "__main__":

    # program parameter:
    # config.path optimizer1 optimizer2

    if len(sys.argv) != 4:
        print("Wrong number of parameter! call: python3 ./main.py /path/to/config.json /path/to/optimizer1 /path/to/optimizer2")
        sys.exit(0)
    config_path = sys.argv[1]
    optimizer1_path = sys.argv[2]
    optimizer2_path = sys.argv[3]

    config = Config(config_path)

    spec1 = importlib.util.spec_from_file_location("opti1", optimizer1_path)
    spec2 = importlib.util.spec_from_file_location("opti2", optimizer2_path)

    module1 = importlib.util.module_from_spec(spec1)
    module2 = importlib.util.module_from_spec(spec2)

    spec1.loader.exec_module(module1)
    spec2.loader.exec_module(module2)

    app = QApplication(sys.argv)
    GUI = App(config, [module1, module2])
    GUI.show()
    sys.exit(app.exec_())
