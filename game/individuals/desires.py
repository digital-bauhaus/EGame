import numpy as np
from game.individuals.trait import Trait

class Desires(Trait):
    def __init__(self, config, dna=None, default=False):
        self.absolute = config['absolute']
        if dna is None:
            if default:
                self.seek_food = config['seek_food']
                self.dodge_poison = config['dodge_poison']
                self.seek_potion = config['seek_potion']
                self.seek_opponents = config['seek_opponents']
                self.seek_corpse = config['seek_corpse']
                self.dodge_predators = config['dodge_predators']
                # self.seek_rainbow_drops = config['seek_rainbow_drops']
                # self.seek_aoe = config['seek_aoe']
                # self.dodge_aoe = config['dodge_aoe']
            else:
                init_values = np.random.dirichlet(np.ones(6), size=1)[0]
                self.seek_food = init_values[0]
                self.dodge_poison = init_values[1]
                self.seek_potion = init_values[2]
                self.seek_opponents = init_values[3]
                self.seek_corpse = init_values[4]
                self.dodge_predators = init_values[5]
        else:
            self.check_dna(dna)
            self.seek_food       = dna[0]
            self.dodge_poison    = dna[1]
            self.seek_potion     = dna[2]
            self.seek_opponents  = dna[3]
            self.seek_corpse     = dna[4]
            self.dodge_predators = dna[5]
    

    def print(self):
        print("seek food", self.seek_food)
        print("dodge poison", self.dodge_poison)
        print("seek potions", self.seek_potion)
        print("seek opponent", self.seek_opponents)
        print("seek corpse", self.seek_corpse)
        print("dodge predators", self.dodge_predators)
    
    def get_dna(self):
        """
        wrap desires into dna array
        """
        return [self.seek_food,
                self.dodge_poison,
                self.seek_potion,
                self.seek_opponents,
                self.seek_corpse,
                self.dodge_predators]
