import numpy as np
class Perception:
    def __init__(self, config, default=False):
        self.absolute_val = config['absolute']
        if default:
            self.food = config['food']
            self.poison = config['poison']
            self.health_potion = config['health_potion']
            self.corpse = config['corpse']
            self.opponent = config['opponent']
            self.predator = config['predator']
            self.rainbow_drop = config['rainbow_drop']
            self.aoe = config['aoe']
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
    
    def absolute(self, type):
        return type * self.absolute_val
