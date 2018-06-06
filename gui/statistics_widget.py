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
        self.setWindowTitle(self.title)
        # print(self.parent.minimumSizeHint().height())
        self.setGeometry(self.left,
                         self.top,
                         self.width,
                         self.height)
        
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(31)  # attributes
        self.table_widget.setColumnCount(20)  # individuals

        self.display_statistics()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
        # self.resize(self.sizeHint().width(), self.sizeHint().height())


        self.show()

    def reload(self, game):
        self.game = game
        self.table_widget.clear()

    def update(self):
        # self.table_widget.clear()
        self.display_statistics()


    def display_statistics(self):
        populations = ["pop1", "pop2"]
        

        header = []
        for pop in populations:
            for i in range(len(self.game.game_objects[pop])):
                header.append(pop + " #" + str(i+1))

        # self.table_widget.setSpan(1,0,7,0)
        # setItem(row, column, item)

        # self.table_widget.setItem(0,0,QTableWidgetItem("Dead"))

        # self.table_widget.setItem(1,0,QTableWidgetItem("Perception"))
        # self.table_widget.setItem(1,1,QTableWidgetItem("Food"))
        # self.table_widget.setItem(2,1,QTableWidgetItem("Poison"))
        # self.table_widget.setItem(3,1,QTableWidgetItem("Heal Potion"))
        # self.table_widget.setItem(4,1,QTableWidgetItem("Corpse"))
        # self.table_widget.setItem(5,1,QTableWidgetItem("Opponent"))
        # self.table_widget.setItem(6,1,QTableWidgetItem("Predator"))


        # self.table_widget.setItem(7,0,QTableWidgetItem("Desires"))
        # self.table_widget.setItem(7,1,QTableWidgetItem("Seek Food"))
        # self.table_widget.setItem(8,1,QTableWidgetItem("Dodge Poison"))
        # self.table_widget.setItem(9,1,QTableWidgetItem("Seek Heal Potion"))
        # self.table_widget.setItem(10,1,QTableWidgetItem("Seek Opponents"))
        # self.table_widget.setItem(11,1,QTableWidgetItem("Seek Corpse"))
        # self.table_widget.setItem(12,1,QTableWidgetItem("Dodge Predators"))

        # self.table_widget.setItem(13,0,QTableWidgetItem("Abilities"))
        # self.table_widget.setItem(13,1,QTableWidgetItem("Increased Armor"))
        # self.table_widget.setItem(14,1,QTableWidgetItem("Increased Speed"))
        # self.table_widget.setItem(15,1,QTableWidgetItem("Increased Poison Resistance"))
        # self.table_widget.setItem(16,1,QTableWidgetItem("Increased Breeding"))
        # self.table_widget.setItem(17,1,QTableWidgetItem("Increased Poisoness"))

        # self.table_widget.setItem(18,0,QTableWidgetItem("Statistics"))
        # self.table_widget.setItem(18,1,QTableWidgetItem("Food Eaten"))
        # self.table_widget.setItem(19,1,QTableWidgetItem("Poison Eaten"))
        # self.table_widget.setItem(20,1,QTableWidgetItem("Consumed Heal Potions"))
        # self.table_widget.setItem(21,1,QTableWidgetItem("Consumed Corpses"))
        # self.table_widget.setItem(22,1,QTableWidgetItem("Attacked Enemies"))
        # self.table_widget.setItem(23,1,QTableWidgetItem("Attacked by Opponents"))
        # self.table_widget.setItem(24,1,QTableWidgetItem("Attacked by Predators"))
        # self.table_widget.setItem(25,1,QTableWidgetItem("Food Seen"))
        # self.table_widget.setItem(26,1,QTableWidgetItem("Poison Seen"))
        # self.table_widget.setItem(27,1,QTableWidgetItem("Heal Potion Seen"))
        # self.table_widget.setItem(28,1,QTableWidgetItem("Opponent Seen"))
        # self.table_widget.setItem(29,1,QTableWidgetItem("Predator Seen"))
        # self.table_widget.setItem(30,1,QTableWidgetItem("Corpse Seen"))

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
