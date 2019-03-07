#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import App
from fastmode import Fastmode
from config import Config
import sys
import importlib.util
import threading

if __name__ == "__main__":

    # program parameter:
    # config.path (optimizer1 optimizer2)

    if len(sys.argv) < 2:
        print("Wrong number of parameter! call: python3 ./main.py ./config.json")
        sys.exit(0)
    config_path = sys.argv[1]
    config = Config(config_path)
    
    # fast mode additional parameter: bool enabled, int runs
    # change if fast mode you need the parameters, otherwise only "python3 ./main.py"
    fastmode = False
    fastmode_runs = 0
    if len(sys.argv) > 4:
        fastmode = sys.argv[4]
        fastmode_runs = int(sys.argv[5])
        threads = []

        optimizer1_path = sys.argv[2]
        optimizer2_path = sys.argv[3] 
        spec1 = importlib.util.spec_from_file_location("opti1", optimizer1_path)
        spec2 = importlib.util.spec_from_file_location("opti2", optimizer2_path)
        module1 = importlib.util.module_from_spec(spec1)
        module2 = importlib.util.module_from_spec(spec2)
        spec1.loader.exec_module(module1)
        spec2.loader.exec_module(module2)    

        for i in range(fastmode_runs):
            thread = Fastmode(i, config, [module1, module2])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join(600) # timeout in seconds 10min = 10*60 = 600
        results = []
        for thread in threads:
            results.append(thread.result)
        yellow = 0
        blue = 0
        too_long_computation = 0
        for result in results:
            if result == 0:
                blue += 1
            elif result == 1:
                yellow += 1
            else:
                too_long_computation += 1
        print("timeout threads (longer than 10min):", too_long_computation)
        if yellow > blue:
            print("yellow wins the competition with " + str(yellow) + ":" + str(blue))
            winning_breeder = optimizer2_path
        elif blue > yellow:
            print("blue wins the competition with " + str(blue) + ":" + str(yellow))
            winning_breeder = optimizer1_path
        else:
            print("we have a draw! " + str(blue) + ":" + str(yellow))
            winning_breeder = "None"
        with open("result.txt", "a") as f:
            # the result of the runs + the path to the winning breeder
            result = "blue:" + str(blue) + " yellow:" + str(yellow) + " OOT:" + str(too_long_computation)
            # 2 = blue, 3 = yellow
            result += " winner: " + winning_breeder
            f.write(result + "\n")

    else:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('./img/game_icon3.png'))
        #GUI = App(config, [module1, module2], fastmode, fastmode_runs)
        GUI = App(config, fastmode, fastmode_runs)
        GUI.show()
        sys.exit(app.exec_())
