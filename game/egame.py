
import numpy as np
from random import uniform
from game.individuals.dot import Dot
from game.individuals.predator import Predator
from game.items.food import Food
from game.items.poison import Poison
from game.items.heal_potion import HealPotion
from game.items.corpse import Corpse

from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import QPoint, Qt

class EGame:

    def __init__(self, parent):
        self.parent = parent
        self.config = self.parent.config
        self.global_parameter = self.config.global_config
        self.predator_config = self.config.predators
        self.num_individuals = self.global_parameter['num_individuals']
        self.num_food = self.global_parameter['num_food']
        self.num_poison = self.global_parameter['num_poison']
        self.num_health_potions = self.global_parameter['num_heal_potion']
        self.spawn_prob_potion = self.global_parameter['spawn_prob_heal_potion']
        self.num_rainbow_drops = self.global_parameter['num_rainbow_drops']
        self.num_predators = self.global_parameter['num_predators']
        self.border_width = self.global_parameter['border_width']
        self.spawn_prob_food = self.global_parameter['spawn_prob_food']
        self.spawn_prob_poison = self.global_parameter['spawn_prob_poison']
        self.spawn_prob_rainbow_drops = self.global_parameter['spawn_prob_rainbow_drops']
        self.spawn_prob_predator = self.global_parameter['spawn_prob_predators']
    
        self.item_config = self.config.items

        self.color_pop1 = (100, 100, 255)
        self.color_pop2 = (255, 165, 0)

        self.game_objects = {}
   
    def start(self):
        self.game_objects['pop1'] = []
        self.game_objects['pop2'] = []
        self.game_objects['food'] = []
        self.game_objects['poison'] = []
        self.game_objects['health_potion'] = []
        self.game_objects['corpse'] = []
        self.game_objects['predators'] = []

        for _ in range(self.num_individuals):
            self.game_objects['pop1'].append(Dot(self.parent, color=self.color_pop1))
            self.game_objects['pop2'].append(Dot(self.parent, color=self.color_pop2))
        for _ in range(self.num_food):
            self.game_objects['food'].append(Food(self.parent, self.border_width))
        for _ in range(self.num_poison):
            self.game_objects['poison'].append(Poison(self.parent, self.border_width))
        for _ in range(self.num_health_potions):
            self.game_objects['health_potion'].append(HealPotion(self.parent, self.border_width))


    def update(self):
        self.update_population(self.game_objects['pop1'], opponent="pop2")
        self.update_population(self.game_objects['pop2'], opponent="pop1")
        self.update_predators(self.game_objects['predators'])
        self.create_objects()
    
    
    def create_objects(self):
        self.create_food()
        self.create_poison()
        self.create_potion()
        self.create_predators()

    
    def create_food(self):
        if (
            uniform(0, 1) < self.spawn_prob_food
            and len(self.game_objects['food']) < self.num_food
        ):
            self.game_objects['food'].append(
                Food(self.parent, self.border_width))

    
    def create_poison(self):
        if (
            uniform(0, 1) < self.spawn_prob_poison
            and len(self.game_objects['poison']) < self.num_poison
        ):
            self.game_objects['poison'].append(
                Poison(self.parent, self.border_width))
    
    
    def create_potion(self):
        if (
            uniform(0, 1) < self.spawn_prob_potion
            and len(self.game_objects['health_potion']) < self.num_health_potions
        ):
            self.game_objects['health_potion'].append(
                HealPotion(self.parent, self.border_width)
            )

    
    def create_predators(self):
        if (
            uniform(0, 1) < self.spawn_prob_predator
            and len(self.game_objects['predators']) < self.num_predators
        ):
            self.game_objects['predators'].append(
                Predator(self.parent, color=self.predator_config['color'])
            )

    
    def update_population(self, population, opponent):
        for i in population:
            if not i.dead:
                i.decrase_health()
                if i.health <= 0.0:
                    self.game_objects["corpse"].append(Corpse(self.parent, 
                                                            self.border_width,
                                                            i.poison,
                                                            position=i._position))
                    i.dead = True
                    continue
                i.increment_survived_time()
                i.seek(self.game_objects, opponent)
                i.stay_in_boundaries(self.border_width)
                i.update()

    
    def update_predators(self, predators):
        for i in predators:
            i.decrase_health()
            if i.health <= 0.0:
                self.game_objects["corpse"].append(Corpse(self.parent,
                                                             self.border_width,
                                                             i.poison,
                                                             position=i._position))
                predators.remove(i)
                continue
            i.seek_populations(self.game_objects, ["pop1", "pop2"])
            i.stay_in_boundaries(self.border_width)
            i.update()
    
    
    def draw(self, painter):
        self.draw_border(painter)
        for f in self.game_objects['food']:
            f.draw(painter)
        for p in self.game_objects['poison']:
            p.draw(painter)
        for p in self.game_objects['pop1']:
            if not p.dead:
                p.draw(painter)
        for p in self.game_objects['pop2']:
            if not p.dead:
                p.draw(painter)
        for h in self.game_objects['health_potion']:
            h.draw(painter)
        for c in self.game_objects['corpse']:
            c.draw(painter)
        for p in self.game_objects['predators']:
            p.draw(painter)

    
    def draw_border(self, painter):
        """draw the inner field where objects are repelled on"""
        if self.parent.parent_window.debug['repell_frame']:
            color = QColor(0, 0, 0, 0)
            w = self.parent.frameGeometry().width()
            h = self.parent.frameGeometry().height()
            position = [w - 2 * self.border_width, h - 2 * self.border_width]
            painter.setBrush(color)
            painter.drawRect(self.border_width, self.border_width, position[0], position[1])
