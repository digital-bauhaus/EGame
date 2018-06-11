import numpy as np

class Ability:
    def __init__(self, ability_base, config, default=False):
        self.armor_dmg_reduce = ability_base['armor_dmg_reduce']
        self.max_speed_increase = ability_base['max_speed_increase']
        if default:
            # increased armor controls how much dmg is taken if attacked
            # 0 means full dmg is taken
            # 1 means full armor_dmg_reduce is applied
            self.increased_armor = config['increased_armor']
            # speed controls additional speed
            # 0 means standard speed is applied
            # 1 means full max_speed_increase is applied
            # (e.g double speed with max_speed_increase = 1)
            self.speed = config['speed']
            # self.poison_resistance = config['poison_resistance']
            # self.reduced_breeding_time = config['reduced_breeding_time']
            # self.poisoness = config['poisoness']
        else:
            init_values = np.random.dirichlet(np.ones(5), size=1)[0]
            self.increased_armor = init_values[0]
            self.speed = init_values[1]
            self.poison_resistance = init_values[2] #TODO
            self.reduced_breeding_time = init_values[3] #TODO
            self.poisoness = init_values[4] #TODO


    def calc_dmg_on_armor(self, dmg):
        """
        applies armor stats to received damage
        """
        # own armor ability * (1 - max percentage armor can reduce) * dmg
        return self.increased_armor * (1 - self.armor_dmg_reduce) * dmg

    def calc_max_speed(self, max_speed):
        """
        applies speed stats to own max speed
        """
        return max_speed + self.speed * self.max_speed_increase

    def print(self):
        print("increased armor ability", self.increased_armor)
        print("speed ability", self.speed)