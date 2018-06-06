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
        self.max_speed = self.max_speed * self.predator_config["speed_factor"]
        self.perception = Perception(self.predator_config["default_perception"], True)
        self.desires = Desires(self.predator_config["default_desires"], True)
        self.radius = self.predator_config['size']

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
       individual.statistic.attacked_by_predators += 1
