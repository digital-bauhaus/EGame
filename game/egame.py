
import numpy as np
from random import uniform, randint, choice
from game.individuals.dot import Dot
from game.individuals.predator import Predator
from game.items.food import Food
from game.items.poison import Poison
from game.items.heal_potion import HealPotion
from game.items.corpse import Corpse
from game.individuals.invalid_population_exception import InvalidPopulationException

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
        self.image_swap_frame = self.global_parameter['image_swap_frame']
    
        self.item_config = self.config.items

        self.breeding_timer = 0
        self.breeder_pop1 = self.parent.parent_window.optimizers[0].Breeder(self.parent)
        self.breeder_pop2 = self.parent.parent_window.optimizers[1].Breeder(self.parent)

        self.colors = {}
        # blueish
        self.colors["pop1"] = [(100, 100, 255), "blue"]
        # orangish
        self.colors["pop2"] = [(255, 165, 0), "yellow"]

        self.game_objects = {}
        self.running = False
        self.frame_counter = 0

    def start(self):
        """
        start the game and initialize all game parameter
        add individuals to populations
        add food | poison | potions
        """
        self.game_objects['pop1'] = []
        self.game_objects['pop2'] = []
        self.game_objects['food'] = []
        self.game_objects['poison'] = []
        self.game_objects['health_potion'] = []
        self.game_objects['corpse'] = []
        self.game_objects['predators'] = []

        self.game_objects['pop1'] = self.breeder_pop1.initialize_population(
            self.num_individuals, self.colors['pop1'])
        self.game_objects['pop2'] = self.breeder_pop2.initialize_population(
            self.num_individuals, self.colors['pop2'])

        # for _ in range(self.num_individuals):
        #     self.game_objects['pop1'].append(Dot(self.parent, color=self.colors['pop1'][0]))
        #     self.game_objects['pop2'].append(Dot(self.parent, color=self.colors['pop2'][0]))
        for _ in range(self.num_food):
            self.game_objects['food'].append(Food(self.parent, self.border_width))
        for _ in range(self.num_poison):
            self.game_objects['poison'].append(Poison(self.parent, self.border_width))
        for _ in range(self.num_health_potions):
            self.game_objects['health_potion'].append(HealPotion(self.parent, self.border_width))
        
        self.running = True


    def update(self):
        """
        update all game elements frame by frame
        increment breeding timer and apply breeding
        """
        self.update_population(self.game_objects['pop1'], opponent="pop2")
        self.update_population(self.game_objects['pop2'], opponent="pop1")
        self.update_predators(self.game_objects['predators'])
        self.create_items()
        self.breeding_timer += 1
        if self.breeding_timer == self.global_parameter['breeding_frame']:
            print("BREEDING TIME")
            self.breed('pop1', breeder=self.breeder_pop1)
            self.breed('pop2', breeder=self.breeder_pop2)
            self.breeding_timer = 0
        self.frame_counter += 1
        # swap the image
        if self.frame_counter == self.image_swap_frame:
            self.frame_counter = 0
            for blue in self.game_objects['pop1']:
                blue.swap_display_image()
            for yellow in self.game_objects['pop2']:
                yellow.swap_display_image()
            for predator in self.game_objects['predators']:
                predator.swap_display_image()
            
    

    def breed(self, population, breeder):
        """
        breed populations with given optimizer
        """
        breeded_population = breeder.breed(self.game_objects[population])
        # check if the population exceeds its individual limit
        if len(breeded_population) > self.num_individuals:
            raise InvalidPopulationException("Population exceeds its maximum individual count!")
        self.game_objects[population] = breeded_population


    
    def create_items(self):
        """
        generate items on the field
        """
        self.create_food()
        self.create_poison()
        self.create_potion()
        self.create_predators()

    
    def create_food(self):
        """
        create food on field if there was some eaten
        """
        if (
            uniform(0, 1) < self.spawn_prob_food
            and len(self.game_objects['food']) < self.num_food
        ):
            self.game_objects['food'].append(
                Food(self.parent, self.border_width))

    
    def create_poison(self):
        """
        create poison on field if there was some eaten
        """
        if (
            uniform(0, 1) < self.spawn_prob_poison
            and len(self.game_objects['poison']) < self.num_poison
        ):
            self.game_objects['poison'].append(
                Poison(self.parent, self.border_width))
    
    
    def create_potion(self):
        """
        create potion on the field if there was some eaten
        """
        if (
            uniform(0, 1) < self.spawn_prob_potion
            and len(self.game_objects['health_potion']) < self.num_health_potions
        ):
            self.game_objects['health_potion'].append(
                HealPotion(self.parent, self.border_width)
            )

    
    def create_predators(self):
        """
        generate predators
        """
        if (
            uniform(0, 1) < self.spawn_prob_predator
            and len(self.game_objects['predators']) < self.num_predators
        ):
            self.game_objects['predators'].append(
                Predator(self.parent, color=[self.predator_config['color'], "brown"])
            )

    
    def update_population(self, population, opponent):
        """
        update all individuals in all populations
        """
        # check variable for end of session
        all_dead = True
        visited = set()
        for i in population:
            if i in visited:
                continue
            visited.add(i)
            # if the individual is not dead
            if not i.dead:
                i.decrase_health()
                if i.health <= 0.0:
                    # generate a corpse at the position where the individual died
                    self.game_objects["corpse"].append(Corpse(self.parent, 
                                                            self.border_width,
                                                            i.poison,
                                                            position=i._position,
                                                            corpse_image=i.corpse_image))
                    i.dead = True
                    continue
                # there is still an individual living
                all_dead = False
                # it survived a frame longer
                i.increment_survived_time()
                # apply seek algorithm
                i.seek(self.game_objects, opponent)
                # apply the boundary force to stay in game area
                i.stay_in_boundaries(self.border_width)
                # apply acceleration to velocity
                i.update()

        # check if all individuals are dead
        if all_dead:
            self.result, self.winner_color = self.end_game()
            # trigger end game screen 
            self.parent.parent_window.game_over(self.winner_color)

    
    def end_game(self):
        # stop the update timer
        self.parent.stop_timer()
        # who wins?
        pops = ["pop1", "pop2"]
        winner = None
        for j in range(len(pops)):
            pop = pops[j]
            all_dead = True
            for i in self.game_objects[pop]:
                if not i.dead:
                    all_dead = False
                    break
            if all_dead:
                print(self.colors[pop][1], "lost")
                winner = (j + 1) % 2
                w_str = self.colors[pops[winner]][1].capitalize()

                self.parent.msg2Statusbar.emit(
                    str("Game Over! " + w_str + " wins!"))
        print("end of game")
        self.running = False
        return winner, w_str
        # TODO: print results to logfile in order to analyze it later

    
    def update_predators(self, predators):
        """
        update all predators
        """
        for i in predators:
            # predators also die in time if they don't eat
            i.decrase_health()
            if i.health <= 0.0:
                # and they spawn a corpse
                self.game_objects["corpse"].append(Corpse(self.parent,
                                                             self.border_width,
                                                             i.poison,
                                                             position=i._position,
                                                             corpse_image=i.corpse_image))
                predators.remove(i)
                continue
            # they only are interested in seeking individuals of all populations
            # and corpses
            i.seek_populations(self.game_objects, ["pop1", "pop2"])
            # apply the boundary force to stay in game area
            i.stay_in_boundaries(self.border_width)
            # apply acceleration to velocity
            i.update()
    
    
    def draw(self, painter):
        """
        draw all game elements on the frame
        """
        if not self.parent.parent_window.fastmode:
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
        # but only if the respective debug setting is enabled
        if self.parent.parent_window.debug['repell_frame']:
            color = QColor(0, 0, 0, 0)
            w = self.parent.frameGeometry().width()
            h = self.parent.frameGeometry().height()
            position = [w - 2 * self.border_width, h - 2 * self.border_width]
            painter.setBrush(color)
            painter.drawRect(self.border_width, self.border_width, position[0], position[1])
