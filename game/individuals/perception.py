import numpy as np
from game.individuals.trait import Trait
class Perception(Trait):
    def __init__(self, config, dna=None, default=False):
        self.absolute_val = config['absolute']
        if dna is None:
            if default:
                self.food = config['food']
                self.poison = config['poison']
                self.health_potion = config['health_potion']
                self.corpse = config['corpse']
                self.opponent = config['opponent']
                self.predator = config['predator']
                # self.rainbow_drop = config['rainbow_drop']
                # self.aoe = config['aoe']
            else:
                init_values = np.random.dirichlet(np.ones(6), size=1)[0]
                self.food = init_values[0]
                self.poison = init_values[1]
                self.health_potion = init_values[2]
                self.opponent = init_values[3]
                self.corpse = init_values[4]
                self.predator = init_values[5]
                # self.rainbow_drop = init_values[6]
                # self.aoe = init_values[7]
        else:
            self.check_dna(dna)
            self.food =          dna[0]
            self.poison =        dna[1]
            self.health_potion = dna[2]
            self.opponent =      dna[3]
            self.corpse =        dna[4]
            self.predator =      dna[5]

    
    def absolute(self, type):
        """
        since the max amount of pixels for perception is configurable
        all perceptions are percentages of the absolute value 
        """
        return type * self.absolute_val

    def print(self):
        print("food perception", self.food)
        print("poison perception", self.poison)
        print("health potion perception", self.health_potion)
        print("corpse perception", self.corpse)
        print("opponent perception", self.opponent)
        print("predator perception", self.predator)

    def get_dna(self):
        """
        wrap perception into dna array
        """
        return [self.food,
                self.poison,
                self.health_potion,
                self.opponent,
                self.corpse,
                self.predator]
