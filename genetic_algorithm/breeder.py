from game.individuals.dot import Dot

from random import choice
from copy import copy

class Breeder:
    def __init__(self, parent):
        self.parent = parent

    def breed(self, population):
        """
        this function gets called by the EGame on one population
        it gets a population consisting of individuals
        each individual has certain statistics and traits
        """
        return self.breed_example(population)

    def initialize_population(self, num_individuals, color):
        """
        this function gets calles by EGame before the first frame
        it gets the number of individuals which have to be generated
        also, it gets the color of the population
        """
        return self.initialize_population_example(num_individuals, color)

    
    def initialize_population_example(self, num_individuals, color):
        """
        example initializer
        creates individuals with random traits
        """
        population = []
        for _ in range(num_individuals):
            population.append(Dot(self.parent, color=color))
        return population


    def breed_example(self, population):
        """
        example breeding function
        simply copy dead individuals traits to a new individual
        """
        population_cpy = copy(population)

        dead = []
        alive = []
        for individual in population_cpy:
            if individual.dead:
                dead.append(individual)
            else:
                alive.append(individual)

        if len(alive) == 0:
            print("END OF BREED")
            return None
        for _ in range(len(dead)):
            dead_individual = choice(dead)
            alive_individual = choice(alive)

            new_individual = Dot(self.parent,
                                 color=dead_individual.color,
                                 position=alive_individual._position,
                                 dna=dead_individual.get_dna())
            population_cpy.append(new_individual)
        for dead_individual in dead:
            population_cpy.remove(dead_individual)
        return population_cpy
