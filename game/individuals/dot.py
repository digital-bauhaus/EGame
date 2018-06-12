from game.individuals.individual import Individual
from game.individuals.perception import Perception
from game.individuals.desires import Desires
from game.individuals.ability import Ability
from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np

class Dot(Individual):
    def __init__(self,
                 parent_canvas,
                 position=None,
                 radius=None,
                 color=None,
                 abilities=None,
                 desires=None,
                 perception=None):
        Individual.__init__(self, parent_canvas, color, radius, position)
        # an individual has perceptions, desires and abilities
        if perception is None:
            self.perception = Perception(self.individual_config['default_perception'],
                                        self.individual_config['use_default_perception'])
        else:
            self.perception = perception
        if desires is None:
            self.desires = Desires(self.individual_config['default_desires'],
                                self.individual_config['use_default_desires'])
        else:
            self.desires = desires
        if abilities is None:
            self.abilities = Ability(self.ability_base,
                                    self.individual_config['default_abilities'],
                                    self.individual_config['use_default_abilities'])
        else:
            self.abilities = abilities
        self.dead = False

    def add_attack_count(self, individual):
        """
        increment the hit counter for the attacked enemy
        """
        individual.statistic.attacked_by_opponents += 1

    def statistic_to_table(self, table_widget, index):
        """
        print individual information to the statistic window
        """
        # setItem(row, column, item)

        table_widget.setItem(0, index, QTableWidgetItem(str(self.dead)))

        #perception
        table_widget.setItem(1, index, QTableWidgetItem(str(self.perception.food)))
        table_widget.setItem(2, index, QTableWidgetItem(str(self.perception.poison)))
        table_widget.setItem(3, index, QTableWidgetItem(str(self.perception.health_potion)))
        table_widget.setItem(4, index, QTableWidgetItem(str(self.perception.corpse)))
        table_widget.setItem(5, index, QTableWidgetItem(str(self.perception.opponent)))
        table_widget.setItem(6, index, QTableWidgetItem(str(self.perception.predator)))

        # #desires
        table_widget.setItem(7, index, QTableWidgetItem(str(self.desires.seek_food)))
        table_widget.setItem(8, index, QTableWidgetItem(str(self.desires.dodge_poison)))
        table_widget.setItem(9, index, QTableWidgetItem(str(self.desires.seek_potion)))
        table_widget.setItem(10, index, QTableWidgetItem(str(self.desires.seek_opponents)))
        table_widget.setItem(11, index, QTableWidgetItem(str(self.desires.seek_corpse)))
        table_widget.setItem(12, index, QTableWidgetItem(str(self.desires.dodge_predators)))

        # #abilities
        table_widget.setItem(13, index, QTableWidgetItem(str(self.abilities.armor_ability)))
        table_widget.setItem(14, index, QTableWidgetItem(str(self.abilities.speed)))
        table_widget.setItem(15, index, QTableWidgetItem(str(self.abilities.poison_resistance)))
        table_widget.setItem(16, index, QTableWidgetItem(str(self.abilities.breeder)))
        table_widget.setItem(17, index, QTableWidgetItem(str(self.abilities.strength)))
        table_widget.setItem(18, index, QTableWidgetItem(str(self.abilities.toxicity)))

        # #statistics
        table_widget.setItem(19, index, QTableWidgetItem(str(self.statistic.food_eaten)))
        table_widget.setItem(20, index, QTableWidgetItem(str(self.statistic.poison_eaten)))
        table_widget.setItem(21, index, QTableWidgetItem(str(self.statistic.consumed_potions)))
        table_widget.setItem(22, index, QTableWidgetItem(str(self.statistic.consumed_corpses)))
        table_widget.setItem(23, index, QTableWidgetItem(str(self.statistic.enemies_attacked)))
        table_widget.setItem(24, index, QTableWidgetItem(str(self.statistic.attacked_by_opponents)))
        table_widget.setItem(25, index, QTableWidgetItem(str(self.statistic.attacked_by_predators)))
        table_widget.setItem(26, index, QTableWidgetItem(str(self.statistic.food_seen)))
        table_widget.setItem(27, index, QTableWidgetItem(str(self.statistic.poison_seen)))
        table_widget.setItem(28, index, QTableWidgetItem(str(self.statistic.potions_seen)))
        table_widget.setItem(29, index, QTableWidgetItem(str(self.statistic.opponents_seen)))
        table_widget.setItem(30, index, QTableWidgetItem(str(self.statistic.predators_seen)))
        table_widget.setItem(31, index, QTableWidgetItem(str(self.statistic.corpses_seen)))

    def print_all_details(self):
        print("is dead", self.dead)
        # desires
        self.desires.print()
        # perceptions
        self.perception.print()
        # abilities
        self.abilities.print()
        # statistics
        self.statistic.print()

    def dmg_dealt(self):
        """
        dmg multiplier is influenced by strength ability
        """
        return self.abilities.calc_dmg_with_strength(1, self.default_dmg)

    def decrase_health(self):
        """
        decrease own health if called
        the amount is increased by own poisoning
        """
        self.health -= self.individual_config['frame_health_reduce'] \
            * self.abilities.calc_poison_reduce(self.poison)
