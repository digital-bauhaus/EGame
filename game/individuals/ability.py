import numpy as np

class Ability:
    def __init__(self, ability_base, config, default=False):
        self.max_dmg_reduce_by_armor = ability_base['armor_dmg_reduce']
        self.max_speed_increase = ability_base['max_speed_increase']
        if default:
            # increased armor controls how much dmg is taken if attacked
            # 0 means full dmg is taken
            # 1 means full armor_dmg_reduce is applied
            self.armor_ability = config['increased_armor']
            # speed controls additional speed
            # 0 means standard speed is applied
            # 1 means full max_speed_increase is applied
            # (e.g double speed with max_speed_increase = 1)
            self.speed = config['speed']
            self.strength = config['strength']
            # self.poison_resistance = config['poison_resistance']
            # self.reduced_breeding_time = config['reduced_breeding_time']
            # self.poisoness = config['poisoness']
        else:
            init_values = np.random.dirichlet(np.ones(6), size=1)[0]
            self.armor_ability = init_values[0]
            self.speed = init_values[1]
            self.strength = init_values[2]
            self.poison_resistance = init_values[2] #TODO
            self.reduced_breeding_time = init_values[3] #TODO
            self.poisoness = init_values[4] #TODO


    def calc_dmg_with_strength(self, dmg):
        """
        applies dmg multiplier to dmg dealt
        """
        return (1 + self.strength) * dmg


    def calc_dmg_on_armor(self, dmg):
        """
        applies armor stats to received damage
        """
        # real_dmg = inc_dmg * (1 - (armor_ability * armor_base))
        return dmg * (1 - self.armor_ability * self.max_dmg_reduce_by_armor)

    def calc_max_speed(self, max_speed):
        """
        applies speed stats to own max speed
        """
        return max_speed + self.speed * self.max_speed_increase

    def print(self):
        print("increased armor ability", self.armor_ability)
        print("speed ability", self.speed)
