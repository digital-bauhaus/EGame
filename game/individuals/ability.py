import numpy as np

class Ability:
    def __init__(self, config, default=False):
        if default:
            self.increased_armor_opponent = config['increased_armor_opponents']
            self.increased_armor_predators = config['increased_armor_predators']
            self.speed = config['speed']
            self.poison_resistance = config['poison_resistance']
            self.reduced_breeding_time = config['reduced_breeding_time']
            self.poisoness = config['poisoness']
        else:
            init_values = np.random.dirichlet(np.ones(6), size=1)[0]
            self.increased_armor_opponent = init_values[0]
            self.increased_armor_predators = init_values[1]
            self.speed = init_values[2]
            self.poison_resistance = init_values[3]
            self.reduced_breeding_time = init_values[4]
            self.poisoness = init_values[5]

