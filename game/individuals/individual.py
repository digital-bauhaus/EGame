import numpy as np
import math
import abc
from random import randint, uniform
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint, QPointF
from game.individuals.perception import Perception
from game.individuals.desires import Desires
from game.individuals.ability import Ability
from game.individuals.statistic import Statistic

class Individual(metaclass=abc.ABCMeta):
    def __init__(self, parent, color, radius=None, position=None):
        self.parent = parent
        self.perception = None
        self.desires = None
        self.abilities = None
        # config parameter
        self.config = self.parent.config
        self.individual_config = self.config.individuals
        self.predator_config = self.config.predators
        self.ability_base = self.config.ability_base
        
        # standard parameter
        self.statistic = Statistic()
        self.max_health = self.individual_config['max_health']
        self.health = self.max_health
        self.poison = self.individual_config['start_poison']
        self.color = color
        self.default_dmg = self.individual_config['default_dmg']

        # if a position was not given
        if position is None:
            _left_border = 0
            _right_border = int(self.parent.frame_dimension[0])
            _top_border = 0
            _bottom_border = int(self.parent.frame_dimension[1])
            _x = float(randint(_left_border, _right_border))
            _y = float(randint(_top_border, _bottom_border))
            self._position = np.array([_x, _y])
        else:
            self._position = np.array([position[0], position[1]])
        # if a radius was given
        if not radius:
            self.radius = self.individual_config['start_size']
        else:
            self.radius = radius
        # let the individuals run in random directions at beginning
        self.acceleration = np.array([uniform(-2,2), uniform(-2,2)])
        self.velocity = np.array([0.0, 0.0])
        self.max_speed = self.individual_config['max_speed']
        self.max_force = self.individual_config['max_force']
        # should the default config be used?

        self.last_tick_seen = {}

    def update(self):
        """update the object by applying acceleration to velocity"""
        # speed up
        self.velocity += self.acceleration
        # the velocity of an object should be limited
        self.velocity = self.limit(self.velocity, self.get_own_max_speed())
        self._position += self.velocity
        # reset acceleration after each iteration
        self.acceleration *= 0


    def apply_force(self, force):
        """
        application of force 
        """
        self.acceleration += force
        self.acceleration = self.limit(self.acceleration, self.get_own_max_speed())


    def seek(self, game_objects, seek_pop):
        """
        calculate the steering vector
        and apply it to the object
        """
        forces = []
        forces.append(self.seek_object(game_objects,
                                       "food",
                                       self.perception.food,
                                       self.eat_food,
                                       self.desires.seek_food))
        forces.append(self.seek_object(game_objects,
                                       "poison",
                                       self.perception.poison,
                                       self.eat_poison,
                                       self.desires.dodge_poison,
                                       inverse=True))
        forces.append(self.seek_object(game_objects,
                                       "health_potion",
                                       self.perception.health_potion,
                                       self.drink_potion,
                                       self.desires.seek_potion))
        forces.append(self.seek_object(game_objects,
                                       seek_pop,
                                       self.perception.opponent,
                                       self.attack_opponent,
                                       self.desires.seek_opponents))
        forces.append(self.seek_object(game_objects,
                                       "corpse",
                                       self.perception.corpse,
                                       self.eat_corpse,
                                       self.desires.seek_corpse))
        forces.append(self.seek_object(game_objects,
                                       "predators",
                                       self.perception.predator,
                                       None,
                                       self.desires.dodge_predators,
                                       inverse=True))
        
        for force in forces:
            if force is not None:
                self.apply_force(force)
        # if there is nothing, move on
        if all(f is None for f in forces):
            # calculate the steering vector
            steer = self.velocity
            # limit the steering
            steer = self.limit(steer, self.max_force)
            self.apply_force(steer)


    def seek_object(self,
                    game_objects,
                    type,
                    perception,
                    eat_callback,
                    desire,
                    inverse=False):
        """
        calculates the force for a given type
        under restriction of the given perception percentage
        and given desire
        if the distance to the next object is covered by own radius
        the element gets eaten if an eat_callback is given
        """
        # get all visible object of the given type
        visible_objects = self.get_visible_objects(
            game_objects, type, perception)
        # set the current visible objects of the given type for statistics
        # keep in mind: visible objects contains tuples as elements
        seen = []
        for element, _ in visible_objects:
            seen.append(element)
        # if we see at least one item
        if len(visible_objects) > 0:
            # iterate over all visible items
            for e in seen:
                # if there is a list for the type and the visible item was not seen in last tick
                if type in self.last_tick_seen and e not in self.last_tick_seen[type]:
                    # increment the counter for the type
                    self.statistic.increment(type)
            # sort visible items with increasing distance
            visible_objects.sort(key=lambda tup: tup[1])
            # get the closest
            closest = visible_objects[0]
            # do we have a function to eat?
            if eat_callback is not None:
                # call that function
                eat_callback(closest, game_objects)
            # set the current visible items to be checked in next frame
            self.last_tick_seen[type] = seen
            # return steering force
            return self.calc_force(closest, desire, inverse)
        # also set current visible items to be checked in next frame
        self.last_tick_seen[type] = seen
        # return none
        return None


    def eat_corpse(self, element, game_objects):
        """
        eat a corpse
        """
        if element[1] - element[0].size/2 <= self.radius:
            self.increase_health(element[0].nutrition)
            self.poison += int(1.0/3.0 * element[0].poison)
            game_objects["corpse"].remove(element[0])
            self.statistic.consumed_corpses += 1


    def drink_potion(self, element, game_objects):
        """
        drink a potion
        """
        if element[1] - element[0].size/2 <= self.radius:
            self.poison = 1
            self.increase_health(0.1)
            game_objects["health_potion"].remove(element[0])
            self.statistic.consumed_potions += 1


    def eat_poison(self, element, game_objects):
        """
        eat poison
        """
        if element[1] - element[0].size/2 <= self.radius:
            self.poison += 1
            game_objects["poison"].remove(element[0])
            self.statistic.poison_eaten += 1


    def eat_food(self, element, game_objects):
        """
        eat some food
        """
        if element[1] - element[0].size/2 <= self.radius:
            self.increase_health(element[0].nutrition)
            game_objects["food"].remove(element[0])
            self.statistic.food_eaten += 1

    @abc.abstractmethod
    def attack_opponent(self, element, game_objects):
        """
        abstract method to attack an individual
        this function differs from dot to predator
        since predators don't have abilities
        """
        pass


    def calc_force(self, element, desire, inverse = False):
        """
        calculate the force under own desire to create the steering vector
        which has to be applied on own acceleration
        """
        target = element[0]._position
        # get the desired vector
        desired = target - self._position
        if inverse:
            desired = - desired
        # set the desired vector length to max
        desired = self.set_magnitude(desired, self.get_own_max_speed())
        # calculate the steering vector
        steer = desired - self.velocity
        # limit the steering
        steer = self.limit(steer, self.max_force) * desire
        # return the steering vector
        return steer


    def decrase_health(self):
        """
        decrease own health if called
        the amount is increased by own poisoning
        """
        self.health -= 0.0005 * self.poison


    def increase_health(self, nutrition):
        """
        increase own health if called by given nutrition
        """
        self.health += nutrition
        if self.health > self.max_health:
            self.health = self.max_health


    def stay_in_boundaries(self, boundary):
        """
        calc and apply force to stay in game area boundaries
        """
        desired = None

        w = self.parent.frameGeometry().width()
        h = self.parent.frameGeometry().height()

        if self._position[0] < boundary:
            desired = self.create_vector(self.get_own_max_speed(), self.velocity[1])
        if self._position[0] > w - 2 * boundary:
            desired = self.create_vector(-self.get_own_max_speed(), self.velocity[1])
        if self._position[1] < boundary:
            desired = self.create_vector(self.velocity[0], self.get_own_max_speed())
        if self._position[1] > h - 2 * boundary:
            desired = self.create_vector(self.velocity[0], -self.get_own_max_speed())
        if desired is not None:
            desired *= self.get_own_max_speed()
            steer = desired - self.velocity
            steer = self.limit(steer, self.max_force/2)
            self.apply_force(steer)


    def get_own_max_speed(self):
        """
        wrapper for individuals / predator max speed calculation
        """
        if self.abilities is not None:
            return self.abilities.calc_max_speed(self.max_speed)
        else:
            return self.max_speed


    def create_vector(self, x, y):
        """
        create a numpy vector for given x and y
        """
        return np.array([x,y])


    def get_visible_objects(self, game_objects, type, perception):
        """
        gets all visible objects in perception radius for a given type
        e.g.:
        type = "food"
        perception = self.perception.food
        """
        visible = []
        p = self.perception.absolute(perception)
        if p < self.radius:
            p = self.radius
        for element in game_objects[type]:
            d = self.dist(self._position, element._position)
            if d <= p:
                if hasattr(element, "dead") and element.dead:
                    pass
                else:
                    visible.append((element, d))
        return visible


    def dist(self, p1, p2):
        """
        calculate distance between two points
        """
        l1 = abs(p1[0] - p2[0])
        l2 = abs(p1[1] - p2[1])
        return math.sqrt(pow(l1, 2) + pow(l2, 2))


    def limit(self, vector, magnitude):
        """
        clip a vector if its length is larger than
        the given magnitude
        """
        # get the magnitude
        length = np.linalg.norm(vector)
        # if magnitude in range return vector
        if length <= magnitude:
            return vector
        # if not: clip the vector
        percentage = magnitude / length
        return vector * percentage


    def set_magnitude(self, vector, magnitude):
        """
        set the length of a vector to the given 
        magnitude by keeping the direction
        """
        length = np.linalg.norm(vector)
        if length == 0:
            return vector
        percentage = magnitude / length
        return vector * percentage


    def increment_survived_time(self):
        """
        individual survived a frame
        """
        self.statistic.time_survived += 1


    @abc.abstractmethod
    def add_attack_count(self, individual):
        """
        abstract method to distinguish between
        wether the given individual was attacked
        by an individual or predator
        """
        pass


    def draw_debug_radius(self, painter, setting, position, color, perception):
        """
        draw the perception radius around the individual
        """
        if self.parent.parent_window.debug[setting]:
            # draw perception
            painter.setPen(QColor(color))
            painter.setBrush(QColor(0, 0, 0, 0))
            painter.drawEllipse(position,
                                self.perception.absolute(
                                    perception),
                                self.perception.absolute(perception))


    def draw_debug_vector(self, painter, setting, position, color, vector):
        """
        draw the given vector on top of the individual
        """
        if self.parent.parent_window.debug[setting]:
            color = QColor(color)
            target = position + QPoint(vector[0]*5, vector[1]*5)
            painter.setBrush(color)
            painter.setPen(QColor("black"))
            painter.drawLine(position, target)


    def draw_debug(self, painter):
        """
        draws all debug elements such as vectors and perceptions
        """
        self.draw_health(painter)
        position = QPoint(self._position[0], self._position[1])
        self.draw_debug_radius(painter,
                               'food_perception',
                               position,
                               'green',
                               self.perception.food)
        self.draw_debug_radius(painter,
                               'poison_perception',
                               position,
                               'red',
                               self.perception.poison)
        self.draw_debug_radius(painter,
                               'potion_perception',
                               position,
                               'violett',
                               self.perception.health_potion)
        self.draw_debug_radius(painter,
                               'opponent_perception',
                               position,
                               'blue',
                               self.perception.opponent)
        self.draw_debug_radius(painter,
                               'predator_perception',
                               position,
                               'black',
                               self.perception.predator)
        self.draw_debug_radius(painter,
                               'corpse_perception',
                               position,
                               'brown',
                               self.perception.corpse)
        self.draw_debug_vector(painter,
                               'velocity_vector',
                               position,
                               "black",
                               self.velocity)


    def draw_health(self, painter):
        """
        draw health on top of the individual
        """
        if self.parent.parent_window.debug['health']:
            # draw health text
            if self.health <= 0.2:
                color = QColor("red")
            else:
                color = QColor("black")
            if self.health >= 0.1:
                position = QPointF(self._position[0]-8, self._position[1]+4)
            else:
                position = QPointF(self._position[0]-4, self._position[1]+4)
            painter.setBrush(color)
            painter.setPen(color)
            if self.health < 1:
                draw_text = str(int(self.health * 100))
                painter.drawText(position, draw_text)


    def draw(self, painter):
        """
        draw the individual
        """
        self.draw_circle(painter)
        self.draw_debug(painter)


    def draw_circle(self, painter):
        """
        draws a circle at own position with own color
        """
        # draw the circle for the individual
        color = QColor(self.color[0], self.color[1], self.color[2])
        position = QPoint(self._position[0], self._position[1])
        painter.setBrush(color)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.drawEllipse(position, self.radius, self.radius)

