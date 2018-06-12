from PyQt5.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem


class StatisticsWidget(QWidget):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.parent = parent
        self.game = game

        self.title = "Statistics"
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 800

        self.initUI()
    

    def initUI(self):
        """
        initialize the widget parameter
        """
        self.setWindowTitle(self.title)
        # print(self.parent.minimumSizeHint().height())
        self.setGeometry(self.left,
                         self.top,
                         self.width,
                         self.height)
        
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(31)  # attributes
        num_individuals = self.parent.parent_window.config.global_config['num_individuals'] * 2
        self.table_widget.setColumnCount(num_individuals)  # individuals

        self.display_statistics()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
        # self.resize(self.sizeHint().width(), self.sizeHint().height())
        self.show()


    def reload(self, game):
        """
        reloads all statistics with the given game instance
        """
        self.game = game
        self.table_widget.clear()


    def update(self):
        """
        redraw statistics
        """
        self.display_statistics()


    def display_statistics(self):
        """
        create a table for statistics for all individuals
        """
        populations = ["pop1", "pop2"]
        
        header = []
        for pop in populations:
            for i in range(len(self.game.game_objects[pop])):
                header.append(self.game.colors[pop][1] + " #" + str(i+1))

        # self.table_widget.setSpan(1,0,7,0)
        # setItem(row, column, item)

        self.table_widget.setHorizontalHeaderLabels(header)
        v_header_labels = [
            "Dead",
            "Food Perception",
            "Poison Perception",
            "Heal Potion Perception",
            "Corpse Perception",
            "Opponent Perception",
            "Predator Perception",
            "Seek Food Desire",
            "Dodge Poison Desire",
            "Seek Heal Potion Desire",
            "Seek Opponents Desire",
            "Seek Corpse Desire",
            "Dodge Predators Desire",
            "Increased Armor",
            "Increased Speed",
            "Increased Poison Resistance",
            "Increased Breeding",
            "Increased Poisoness",
            "Food Eaten",
            "Poison Eaten",
            "Consumed Heal Potions",
            "Consumed Corpses",
            "Attacked Enemies",
            "Attacked by Opponents",
            "Attacked by Predators",
            "Food Seen",
            "Poison Seen",
            "Heal Potion Seen",
            "Opponent Seen",
            "Predator Seen",
            "Corpse Seen"
        ]
        self.table_widget.setVerticalHeaderLabels(v_header_labels)
        pop_offset = 0
        for pop in populations:
            index = 0
            for individual in self.game.game_objects[pop]:
                individual.statistic_to_table(
                    self.table_widget, pop_offset+index)
                index += 1
            pop_offset += len(self.game.game_objects[pop])
