import numpy as np

class Ability:
    def __init__(self, ability_base, config, default=False):
        self.armor_dmg_reduce = ability_base['armor_dmg_reduce']
        if default:
            # increased armor controls how much dmg is taken if attacked
            # 0 means full dmg is taken
            # 1 means full armor_dmg_reduce is applied
            self.increased_armor = config['increased_armor']
            self.speed = config['speed']
            self.poison_resistance = config['poison_resistance']
            self.reduced_breeding_time = config['reduced_breeding_time']
            self.poisoness = config['poisoness']
        else:
            init_values = np.random.dirichlet(np.ones(5), size=1)[0]
            self.increased_armor = init_values[0]
            self.speed = init_values[1]
            self.poison_resistance = init_values[2]
            self.reduced_breeding_time = init_values[3]
            self.poisoness = init_values[4]


    def calc_dmg_on_armor(self, dmg):
        """
        applies armor stats to received damage
        """
        # own armor ability * (1 - max percentage armor can reduce) * dmg
        return self.increased_armor * (1 - self.armor_dmg_reduce) * dmg
