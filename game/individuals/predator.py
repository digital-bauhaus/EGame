from game.individuals.individual import Individual
from game.individuals.desires import Desires
from game.individuals.perception import Perception
from random import randint, uniform
import numpy as np

class Predator(Individual):
    def __init__(self,
                 parent,
                 position=None,
                 radius=None,
                 color=None):
        Individual.__init__(self, parent, color, radius, position)
        # a predator is slower than individuals
        self.max_speed = self.max_speed * self.predator_config["speed_factor"]
        # it has perceptions and desires defined in config file
        self.perception = Perception(self.predator_config["default_perception"], True)
        self.desires = Desires(self.predator_config["default_desires"], True)
        self.radius = self.predator_config['size']

        self.default_dmg = self.predator_config['default_dmg']

        # we want that the predators spawn outside of the game area        
        _left_border = 0
        _right_border = int(self.parent.frame_dimension[0])
        _top_border = 0
        _bottom_border = int(self.parent.frame_dimension[1])
        _xa = float(randint(-100, _left_border))
        _xb = float(randint(_right_border, _right_border + 100))
        if uniform(0, 1) < 0.5:
            _x = _xa
        else:
            _x = _xb
        _ya = float(randint(-100, _top_border))
        _yb = float(randint(_bottom_border, _bottom_border + 100))
        if uniform(0, 1) < 0.5:
            _y = _ya
        else:
            _y = _yb
        self._position = np.array([_x, _y])

    def add_attack_count(self, individual):
       """
       increment the hit counter for the attacked enemy
       """
       individual.statistic.attacked_by_predators += 1

    def seek_populations(self, game_objects, opponents):
        """
        seek elements called by predators
        """
        force_applied = False
        for pop in opponents:
            opponent_force = self.seek_object(game_objects,
                                              pop,
                                              self.perception.opponent,
                                              self.attack_opponent,
                                              self.desires.seek_opponents)
            if opponent_force is not None:
                self.apply_force(opponent_force)
                force_applied = True
        corpse_force = self.seek_object(game_objects,
                                        "corpse",
                                        self.perception.corpse,
                                        self.eat_corpse,
                                        self.desires.seek_corpse)
        if corpse_force is not None:
            self.apply_force(corpse_force)
            force_applied = True
            self.poison = 1
        if not force_applied:
            # calculate the steering vector
            steer = self.velocity * 100
            # limit the steering
            # steer = self.set_magnitude(steer, self.max_force)
            self.apply_force(steer)

    def dmg_dealt(self):
        """
        dmg is simply the default value
        """
        return self.default_dmg

    def decrase_health(self):
        """
        decrease own health if called
        the amount is increased by own poisoning
        """
        self.health -= self.individual_config['frame_health_reduce'] * self.poison
